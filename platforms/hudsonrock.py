# platforms/hudsonrock.py
import requests
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def check_hudsonrock(username):
    """
    Query Hudson Rock OSINT API for a username and return parsed results.
    """
    url = f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-username?username={username}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code != 200:
            return [{"platform": "HudsonRock", "error": f"HTTP {res.status_code}"}]

        data = res.json()

        # If API returned an error message or no stealers
        if not data or "stealers" not in data or not data["stealers"]:
            return [{"platform": "HudsonRock", "error": "No records found"}]

        results = []
        for entry in data["stealers"]:
            results.append({
                "platform": "HudsonRock",
                "date_compromised": datetime.strptime(entry.get("date_compromised", ""), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S") if entry.get("date_compromised") else None,
                "stealer_family": entry.get("stealer_family"),
                "computer_name": entry.get("computer_name"),
                "operating_system": entry.get("operating_system"),
                "malware_path": entry.get("malware_path"),
                "ip": entry.get("ip"),
                "total_corporate_services": entry.get("total_corporate_services"),
                "total_user_services": entry.get("total_user_services"),
                "top_passwords": ", ".join(entry.get("top_passwords", [])),
                "top_logins": ", ".join(entry.get("top_logins", [])),
                "profile_url": "https://www.hudsonrock.com/free-tools"  
            })

        return results

    except Exception as e:
        return [{"platform": "HudsonRock", "error": str(e)}]
