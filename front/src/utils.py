import requests

# Returns a tuple, first boolean indicates request success, second is an optional dictionary. If it fails it will return (False, None)
def response_handler(response: requests.Response) -> tuple[bool, dict | None]:
    try:
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.HTTPError as e:
        print("HTTP error occurred:", e)
    except requests.exceptions.RequestException as e:
        print("A request error occurred:", e)
    except Exception as e:
        print("Unexpected error:", e)
    return False, None