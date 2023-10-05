# MIT License
#
# Copyright (c) 2023 Tim Kelly
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import requests
from datetime import datetime
import pandas as pd
import json

# scanning modules function imports
from scan_modules.robots_txt_scanner import check_robots_txt
from scan_modules.ip_collect_scanner import check_ip_addresses
from scan_modules.sec_headers_scan import check_security_headers
from scan_modules.http_result_scan   import check_http_response
from scan_modules.firewal_scan import detect_firewall
from scan_modules.screen_shot_scan import take_screenshot

# Regular expressions and their corresponding types for PII patterns
pii_patterns = [
    (r"\b\d{3}-\d{2}-\d{4}\b", "SSN"),
    (r"\b\d{4}-\d{4}-\d{4}-\d{4}\b", "Credit Card"),
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "Email"),
    (r"\bpassword\s*=\s*['\"](.*?)['\"]", "Password"),
    (r"\bprivate_key\s*=\s*['\"](.*?)['\"]", "Private Key"),
]

try:
    with open("rekon-config.json", "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print("Error: The 'rekon-config.json' file does not exist.")
except json.JSONDecodeError as e:
    print(f"Error: Failed to parse 'rekon-config.json'. JSON decoding error: {e}")
    # You can add additional error handling for JSON decoding errors if needed
    # For example, you might want to print e.msg and e.lineno to provide more information
    # about the specific error.
    # e.g., print(f"Error at line {e.lineno}: {e.msg}")
    exit(1)  # Exit the program with an error code
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit(1)  # Exit the program with an error code

# Initialize an empty list to store data frames for each ROOT_DOMAIN
dfs = []
aggregate_df = []

def start_scan(urls_to_scan):
    
    for ROOT_DOMAIN in urls_to_scan:

        print("Scanning: " +  ROOT_DOMAIN)

        RECORD_LIMIT = config["max_dns_records"]

        print(f"∞∞∞∞∞ Start rekon for {ROOT_DOMAIN}. . . ")

        crt_sh_url = f"https://crt.sh/?q={ROOT_DOMAIN}&output=json&deduplicate=Y"
        response = requests.get(crt_sh_url)
        certificates = response.json()

        dns_names = {}
        rows_parsed = 0  # Counter for the number of rows parsed
        data = []

        for cert in certificates:
            if rows_parsed >= RECORD_LIMIT:
                break  # Exit the loop if the desired number of rows has been parsed

            crtsh_id = cert["id"]
            logged_at = cert["entry_timestamp"]
            not_before = cert["not_before"]
            not_after = cert["not_after"]
            common_name = cert["common_name"]
            issuer_name = cert["issuer_name"]

            if common_name not in dns_names or dns_names[common_name]["not_after"] > not_after:
                dns_names[common_name] = {
                    "crtsh_id": crtsh_id,
                    "logged_at": logged_at,
                    "not_before": not_before,
                    "not_after": not_after,
                    "issuer_name": issuer_name,
                }

                rows_parsed += 1

                data.append([crtsh_id, logged_at, not_before, not_after, common_name, issuer_name])

        columns = ["CRTSH ID", "Logged At", "Not Before", "Not After", "Common Name", "Issuer Name"]
        df = pd.DataFrame(data, columns=columns)

        # Append the data frame to the list
        dfs.append(df)


def is_valid_domain(domain):
    return not domain.startswith("*.") and "." in domain

# Function to write DataFrame to a CSV file
def write_to_csv(dataframe, filename):
    try:
        dataframe.to_csv(filename, index=False)
        print(f"DataFrame has been successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing to {filename}: {e}")

start_scan(config["root_urls"])

# Concatenate all data frames in the list into one
aggregate_df = pd.concat(dfs, ignore_index=True)

# The result is a new DataFrame deduplicated_df that contains only the earliest certificates for each unique "Common Name," 
# effectively deduplicating the data based on the "Common Name" column. This is because we will have multiple certificates
#  for the same domain, and we only want to retain only the most recent one.
deduplicated_df = aggregate_df.sort_values(by=["Common Name", "Not After"], ascending=[True, False]) \
    .groupby("Common Name").head(1)

# Get all the DNS names into an array. Then we can start the actually scanning
dns_names_list = deduplicated_df["Common Name"].tolist()

if config["run_firewall_scan"]:

    print(f"Starting firewall scan . . .")
    firewall_results = []

    for dns_name in dns_names_list:
        if is_valid_domain(dns_name):
            firewall_result = detect_firewall(dns_name)
            firewall_results.append(firewall_result)
        else:
            firewall_results.append("DNT")

    deduplicated_df["firewall"] = firewall_results

if config["run_ip_scan"]:

    print(f"Starting IP gathering scan . . .")
    found_ips = []

    for dns_name in dns_names_list:
        if is_valid_domain(dns_name):
            ip_result = check_ip_addresses(dns_name)
            found_ips.append(ip_result)
        else:
            found_ips.append("DNT")

    deduplicated_df["associated_ips"] = found_ips

if config["http_status_scan"]:

    print(f"Starting HTTP response scan  . . .")
    http_responses = []  # Store HTTP responses

    for dns_name in dns_names_list:
        if is_valid_domain(dns_name):
            http_result = check_http_response(dns_name)
            http_responses.append(http_result)  # Append the HTTP response code
        else:
            http_responses.append("DNT")

    # Add a new column "http_response" to deduped_df
    deduplicated_df["http_response"] = http_responses

if config["sec_headers_scan"]:

    print(f"Starting security headers check . . .")
    sec_header_responses = []  # Store security header results

    for dns_name in dns_names_list:
        if is_valid_domain(dns_name):
            sec_header_result = check_security_headers(dns_name)
            sec_header_responses.append(sec_header_result)  # Append the security header result
        else:
            sec_header_responses.append("DNT") 

    # Add a new column "missing_sec_headers" to deduplicated_df
    deduplicated_df["missing_sec_headers"] = sec_header_responses

if config["run_robots_txt_scan"]:

    print(f"Starting robots.txt scan . . .")
    robots_text_response = []

    for dns_name in dns_names_list:
        if is_valid_domain(dns_name):
            robots_text_result = check_robots_txt(dns_name)
            robots_text_response.append(robots_text_result)  # Append the security header result
        else:
            robots_text_response.append("DNT")

    # Add a new column "missing_sec_headers" to deduplicated_df
    deduplicated_df["has_robots_txt"] = robots_text_response

# Get the current date in the "YYYYMMDD" format
current_date = datetime.now().strftime("%Y%m%d")

# Update the csv_filename with the current date
csv_filename = f"scan_results_{current_date}.csv"

print(f"Writing output results . . .")
# Call the function to write the DataFrame to the CSV file
write_to_csv(deduplicated_df, csv_filename)

if config["take_screenshot"]:

    print(f"Starting screenshots scan . . .")
    
    for dns_name in dns_names_list:
        if is_valid_domain(dns_name):
             take_screenshot(dns_name)

print(f"√ rekon complete . . . ")

