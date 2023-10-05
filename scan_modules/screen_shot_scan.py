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

