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
from requests.exceptions import SSLError, ConnectionError, ReadTimeout
from urllib3.exceptions import NewConnectionError
import time

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