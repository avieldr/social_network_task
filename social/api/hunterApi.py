import requests

HUNTER_API_KEY = "9a4f33a87fa58c6b2a7ed9d7824cc0200407de89"
INVALID = "invalid"

def verifyEmail(email):
        url = "https://api.hunter.io/v2/email-verifier?email={}&api_key={}".format(email, HUNTER_API_KEY)
        response = requests.get(url)
        return response.status_code, response.json()