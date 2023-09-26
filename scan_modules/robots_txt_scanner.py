# robots_txt_scanner.py

import requests

def check_robots_txt(common_name):
    common_name = common_name.strip()
    found_robots_txt = False

    try:
        response = requests.get(f"https://{common_name}/robots.txt", timeout=10)
        http_response = response.status_code

        if http_response == 200:
            found_robots_txt = True
    except Exception as e:
        pass  # Handle any exceptions if needed

    return found_robots_txt
