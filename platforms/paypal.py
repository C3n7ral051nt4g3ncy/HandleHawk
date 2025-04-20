import requests
import json
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def extract_json_from_script(soup, script_id):
    script_tag = soup.find("script", {"id": script_id})
    if script_tag:
        try:
            return json.loads(script_tag.string)
        except json.JSONDecodeError:
            return None
    return None

def check_paypal(username):
    url = f"https://www.paypal.me/{username}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code != 200 or "doesn't exist" in res.text:
            return [{"platform": "PayPal", "error": "No profile found"}]

        soup = BeautifulSoup(res.text, "html.parser")
        data = extract_json_from_script(soup, "client-data")
        if not data:
            return [{"platform": "PayPal", "error": "Profile metadata not found"}]

        user_info = data.get("recipientSlugDetails", {}).get("slugDetails", {}).get("userInfo", {})
        profile = {
            "platform": "PayPal",
            "full_name": user_info.get("displayName", ""),
            "first_name": user_info.get("givenName", ""),
            "last_name": user_info.get("familyName", ""),
            "bio": user_info.get("description", ""),
            "avatar": user_info.get("profilePhotoUrl", ""),
            "currency": user_info.get("primaryCurrencyCode", ""),
            "profile_url": url,
        }
        return [profile]

    except Exception as e:
        return [{"platform": "PayPal", "error": str(e)}]
