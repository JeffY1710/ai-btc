import requests

# Returns a tuple, first boolean indicates request success, second is an optional dictionary. If it fails it will return (False, None)
def response_handler(method: str, url: str, **kwargs) -> tuple[bool, dict | None]:
    try:
        response = requests.request(method=method, url=url, **kwargs)
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.HTTPError as e:
        print("HTTP error occurred:", e, method, url, kwargs)
    except requests.exceptions.RequestException as e:
        print("A request error occurred:", method, url, kwargs)
    except Exception as e:
        print("Unexpected error:", e)
    return False, None