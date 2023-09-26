import requests

COMMON_SECURITY_HEADERS = [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Frame-Options",
        "Referrer-Policy",
    ]

def has_security_misconfiguration(headers):
    missing_headers = [
        header for header in COMMON_SECURITY_HEADERS if header not in headers
    ]
    return missing_headers

# Define the function to check security headers
def check_security_headers(common_name):
    common_name = common_name.strip()
    missing_headers_str = ""

    try:
        response = requests.get(f"https://{common_name}", timeout=10)
        http_response = response.status_code

        if http_response >= 400:
            missing_headers_str = "DNT"

        headers = response.headers
        missing_headers = has_security_misconfiguration(headers)

        if missing_headers:
            missing_headers_str = ",".join(missing_headers)
        else:
            missing_headers_str = "No missing headers"

    except (
        SSLError,
        ConnectionError,
        NewConnectionError,
        ReadTimeout,
    ) as error:
        print(f"Error for {common_name}: {error}")
        time.sleep(1)  # Wait before retrying
        missing_headers_str = "Error: " + str(error)

    return missing_headers_str