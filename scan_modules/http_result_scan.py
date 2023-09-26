import requests

# HTTP response
def check_http_response(common_name):
    common_name = common_name.strip().lower()  # Convert to lowercase
    url = f"http://{common_name}"

    try:
        response = requests.get(url, timeout=10)
        return response.status_code

    except requests.exceptions.RequestException:
        return "999"  # Return 999 for exceptions