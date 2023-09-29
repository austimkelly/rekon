# Define the function for firewall detection
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

import subprocess
import re

def identify_firewall(domain):
        command = f"wafw00f {domain}"
        result = subprocess.check_output(command, shell=True, text=True)
        return result.strip()

def detect_firewall(domain):
    
    firewall_result = "Unknown"  # Initialize with None by default
    firewall_result_raw = identify_firewall(domain)
    firewall_lines = firewall_result_raw.split('\n')

    for line in firewall_lines:
        if "No WAF detected" in line:
            firewall_result = "No WAF detected"
            break
        elif "is behind" in line:
            firewall_result = clean_firewall_name(line.split("is behind", 1)[1].strip())
            break

    return firewall_result

def clean_firewall_name(name):
    return re.sub(r"\x1b\[\d+;\d+m", "", name)