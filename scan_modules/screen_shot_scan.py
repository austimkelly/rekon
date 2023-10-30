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
import os
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def normalize_url(url):
    # Add 'https://' to the URL if not already present
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def take_screenshot(url, output_dir='screen_captures'):

    # Normalize the URL
    url = normalize_url(url)

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode (no GUI)
    
    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    output_filename = "DNT"

    try:
        # Navigate to the URL
        driver.get(url)
        
        # Extract the domain from the URL for filename
        domain = urlparse(url).netloc.replace('.', '_')
        
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Specify the output file name
        output_filename = os.path.join(output_dir, f'{domain}_screenshot.png')
        
        # Take a screenshot
        driver.save_screenshot(output_filename)
        print(f'Screenshot saved to {output_filename}')
    
    except Exception as e:
        print(f"Unable to get screenshot for : {url}")
    
    finally:
        # Close the WebDriver
        driver.quit()

    return output_filename
