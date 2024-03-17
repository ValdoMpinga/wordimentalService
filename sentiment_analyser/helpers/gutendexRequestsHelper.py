import urllib.request
import json


def getRequest(url):
    try:
        # Make the request using urllib
        with urllib.request.urlopen(url) as response:
            # Read the response content
            response_content = response.read()
            # Decode JSON response
            data = json.loads(response_content)
            return data
    except urllib.error.HTTPError as e:
        # Handle HTTP errors (e.g., 404 Not Found)
        raise Exception(f"Failed to retrieve data from {url}: {e}")
    except Exception as e:
        # Handle other errors
        raise Exception(f"Failed to retrieve data from {url}: {e}")

