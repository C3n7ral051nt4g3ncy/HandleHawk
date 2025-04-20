#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HandleHawk - Cross-platform Username Recon Tool
# Written in Python 🐍
# Black Code Formatter (https://github.com/psf/black)
# By C3n7ral051nt4g3ncy (https://github.com/C3n7ral051nt4g3ncy)

import requests
import json
from datetime import datetime
from html import unescape
import re
import sys
import time
import threading
from bs4 import BeautifulSoup
from bech32 import bech32_encode, convertbits

#Added platforms after version 1.0
from platforms import paypal


# cloudscraper for cloudfare bypass
try:
    import cloudscraper

    USE_CLOUDSCRAPER = True
except ImportError:
    USE_CLOUDSCRAPER = False


# Spinner
class Spinner:
    def __init__(self, message="Working"):
        self.message = message
        self.done = False
        self.spinner_thread = threading.Thread(target=self.spin)
        self.chars = ["|", "/", "-", "\\"]

    def spin(self):
        i = 0
        while not self.done:
            sys.stdout.write(
                f"\r🔄 {self.message}... {self.chars[i % len(self.chars)]}"
            )
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write(f"\r✅ {self.message}... Done!\n")

    def start(self):
        self.done = False
        self.spinner_thread.start()

    def stop(self):
        self.done = True
        self.spinner_thread.join()


# Headers to avoid detection as a bot/automated script
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
}

# ANSI Colors
RESET = "\033[0m"
GREEN = "\033[32m"
PURPLE = "\033[34m"
WHITE = "\033[97m"

# ascii art
hawk_ascii = rf"""
{PURPLE}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣲⣶⠒⠷⠶⠤⠴⠦⠤⠤⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣴⣶⠚⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⢌⣛⠶⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢚⠟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠱⡄⠙⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠖⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣀⠀⣀⣤⣧⠔⠛⠓⠲⠤⢄⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣤⣄⣠⣤⣴⣾⣿⣿⣾⡗⠀⢀⣀⢤⠐⠠⠤⣉⠓⠦⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠒⠶⠶⢾⣿⡿⠛⢻⣻⠛⢻⣿⣿⠟⣋⣺⣿⠏⠀⠴⠿⠹⠋⠀⠀⠀⠀⠈⠀⠨⠳⣄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢐⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣤⠤⠄⠐⢾⣿⣝⠤⣀⢀⡠⣱⣿⣿⣿⣿⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡆⠀
⠀⠀⠀⠀⠀⠀⢠⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢉⣛⣺⣿⣾⣛⣽⣿⡟⠁⠀⠀⢀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡀
⠀⠀⠀⠀⠀⠐⡟⠀⠀⠀⠀⡠⠖⠀⠀⠀⢀⡴⠃⠀⠀⠀⠀⠀⠀⡈⠉⢉⡽⠿⢛⡿⢛⠯⠭⣒⣚⣩⣭⣭⣤⡤⠭⠭⢭⣥⣀⣉⣑⣒⢵⡀⠀⠀⢸⡇
⠀⠀⠀⠀⠀⣰⠃⠀⢀⡔⠋⠀⠀⠀⣠⡴⠋⠀⠀⠀⠀⣠⣤⡴⠋⠀⠀⠀⠀⠀⠾⢶⣾⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠳⡀⠀⣸⠃
⠀⠀⠀⠀⢰⠟⢀⣴⠏⠀⡀⢀⣴⡿⠋⠀⠀⠀⢀⡴⠟⠋⠁⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣇⠔⠁⠀
⠀⠀⠀⠀⣞⣴⣿⠃⢠⣾⣴⣿⠋⠀⠀⠀⠀⠐⠋⠀⠀⠀⠀⠀⢐⣚⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⠁⠀⠀⠀
⠀⠀⠀⣸⣿⣿⣧⣶⣿⣿⣿⠗⠁⠀⡠⠂⠀⢀⠀⠀⠀⠀⠂⢉⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⡟⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

{RESET}{WHITE}  _    _                 _ _      _    _                _    
 | |  | |               | | |    | |  | |              | |   
 | |__| | __ _ _ __   __| | | ___| |__| | __ ___      _| | __
 |  __  |/ _` | '_ \ / _` | |/ _ \  __  |/ _` \ \ /\ / / |/ /
 | |  | | (_| | | | | (_| | |  __/ |  | | (_| |\ V  V /|   < 
 |_|  |_|\__,_|_| |_|\__,_|_|\___|_|  |_|\__,_| \_/\_/ |_|\_\{RESET}

{GREEN} HandleHawk 🦅  Multi-platform User Recon 🔎 {RESET}                                
{PURPLE} Version 1.1 {RESET}
"""
print(hawk_ascii)


# Strip HTML Tags
def strip_html_tags(text):
    return re.sub(r"<[^<]+?>", "", unescape(text or ""))


# Bluesky check function
def check_bluesky(username):
    url = f"https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={username}.bsky.social"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        return [
            {
                "platform": "Bluesky",
                "handle": data.get("handle"),
                "display_name": data.get("displayName") or data.get("handle"),
                "avatar": data.get("avatar"),
                "created_at": data.get("createdAt"),
                "followers": data.get("followersCount"),
                "following": data.get("followsCount"),
                "posts": data.get("postsCount"),
                "profile_url": f"https://bsky.app/profile/{data.get('handle')}",
            }
        ]
    return [{"platform": "Bluesky", "error": "No profile found"}]

# convert hex to npub to get the profile link
def hex_to_npub(hex_key):
    """Convert hex pubkey to npub format for nostrapp.link"""
    data = convertbits(bytes.fromhex(hex_key), 8, 5)
    return bech32_encode("npub", data)

# Nostr check function
def check_nostr(username):
    base_url = "https://api.nostr.wine/search"
    page = 1
    profiles = []

    while True:
        url = f"{base_url}?query={username}&page={page}"
        print(f"\r🔄 Checking Nostr (page {page})...", end="")
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            if res.status_code == 429:
                print(f"\n⏳ Rate limited on page {page}. Waiting 10 seconds...")
                time.sleep(10)
                continue

            if res.status_code != 200:
                break

            data = res.json()
            page_results = data.get("data", [])
            for item in page_results:
                if item.get("kind") != 0:
                    continue
                try:
                    content = json.loads(item.get("content", ""))
                except json.JSONDecodeError:
                    continue

                pubkey = item.get("pubkey", "")
                npub = hex_to_npub(pubkey) if pubkey else ""
                profiles.append({
                    "platform": "Nostr",
                    "name": content.get("name", ""),
                    "display_name": content.get("display_name", ""),
                    "about": content.get("about", ""),
                    "avatar": content.get("picture", ""),
                    "website": content.get("website", ""),
                    "nip05": content.get("nip05", ""),
                    "created_at": (
                        datetime.utcfromtimestamp(item.get("created_at")).strftime("%Y-%m-%d %H:%M:%S")
                        if item.get("created_at") else ""
                    ),
                    "profile_url": f"https://nostrapp.link/{npub}" if npub else ""
                })

            pagination = data.get("pagination", {})
            total_pages = pagination.get("total_pages", page)
            if pagination.get("last_page", True) or page >= total_pages:
                print(f"\r✅ Nostr check complete ({page}/{total_pages})")
                break
            time.sleep(1.5) 
            page += 1
        except Exception as e:
            print(f"\r❌ Error checking Nostr (page {page}): {str(e)}")
            break

    return profiles or [{"platform": "Nostr", "error": "No profile found"}]


# Mastodon check function
def check_mastodon(username):
    url = f"https://mastodon.social/api/v2/search?q={username}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        return [{"platform": "Mastodon", "error": "No profile found"}]
    try:
        accounts = res.json().get("accounts", [])
        matches = []
        for acct in accounts:
            if acct.get("username", "").lower() != username.lower():
                continue
            matches.append(
                {
                    "platform": "Mastodon",
                    "display_name": acct.get("display_name", ""),
                    "username": acct.get("username", ""),
                    "acct": acct.get("acct", ""),
                    "bio": strip_html_tags(acct.get("note", "")),
                    "profile_url": acct.get("url", ""),
                    "avatar": acct.get("avatar", ""),
                    "banner": acct.get("header", ""),
                    "created_at": acct.get("created_at", ""),
                    "followers": acct.get("followers_count", 0),
                    "following": acct.get("following_count", 0),
                    "posts": acct.get("statuses_count", 0),
                }
            )
        return matches or [{"platform": "Mastodon", "error": "No profile found"}]
    except:
        return [{"platform": "Mastodon", "error": "No profile found"}]


# Truthsocial check function
def check_truthsocial(username):
    url = f"https://truthsocial.com/api/v1/accounts/lookup?acct={username}"
    try:
        if USE_CLOUDSCRAPER:
            scraper = cloudscraper.create_scraper()
            res = scraper.get(url, headers=HEADERS, timeout=10)
        else:
            session = requests.Session()
            session.headers.update(HEADERS)
            res = session.get(url, timeout=10)

        if res.status_code != 200:
            return [{"platform": "TruthSocial", "error": "No profile found"}]

        acct = res.json()
        return [
            {
                "platform": "TruthSocial",
                "display_name": acct.get("display_name", ""),
                "username": acct.get("username", ""),
                "acct": acct.get("acct", ""),
                "bio": strip_html_tags(acct.get("note", "")),
                "profile_url": acct.get("url", ""),
                "avatar": acct.get("avatar", ""),
                "banner": acct.get("header", ""),
                "created_at": acct.get("created_at", ""),
                "followers": acct.get("followers_count", 0),
                "following": acct.get("following_count", 0),
                "posts": acct.get("statuses_count", 0),
                "website": acct.get("website", ""),
                "verified": "✅ Yes" if acct.get("verified") else "❌ No",
            }
        ]
    except:
        return [{"platform": "TruthSocial", "error": "No profile found"}]


# Reddit check function
def check_reddit(username):
    url = f"https://www.reddit.com/user/{username}/about.json"
    res = requests.get(url, headers=HEADERS)

    if res.status_code != 200:
        return [{"platform": "Reddit", "error": "No profile found"}]

    try:
        data = res.json().get("data", {})
        return [
            {
                "platform": "Reddit",
                "username": data.get("name", ""),
                "profile_url": f"https://www.reddit.com/user/{data.get('name')}",
                "avatar": data.get("icon_img", ""),
                "created_at": (
                    datetime.utcfromtimestamp(data.get("created_utc")).strftime(
                        "%Y-%m-%d"
                    )
                    if data.get("created_utc")
                    else ""
                ),
                "total_karma": data.get("total_karma", 0),
                "link_karma": data.get("link_karma", 0),
                "comment_karma": data.get("comment_karma", 0),
                "verified": "✅ Yes" if data.get("verified") else "❌ No",
            }
        ]
    except:
        return [{"platform": "Reddit", "error": "No profile found"}]


# X Twitter API via RapidAPI (optional)
def check_twitter_via_api(username, api_key=None):
    if not api_key:
        print("⚠️  Twitter API key not provided, skipping Twitter check.")
        return []

    url = f"https://twitter-api45.p.rapidapi.com/screenname.php?screenname={username}"
    headers = {
        "x-rapidapi-host": "twitter-api45.p.rapidapi.com",
        "x-rapidapi-key": api_key,
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return [{"platform": "Twitter", "error": f"HTTP {res.status_code}"}]
        data = res.json()
        return [
            {
                "platform": "Twitter",
                "display_name": data.get("name"),
                "username": username,
                "bio": data.get("desc", ""),
                "profile_url": f"https://twitter.com/{username}",
                "avatar": data.get("avatar"),
                "banner": data.get("header_image"),
                "created_at": data.get("created_at"),
                "followers": data.get("sub_count"),
                "following": data.get("friends"),
                "posts": data.get("statuses_count"),
                "verified": "✅ Yes" if data.get("blue_verified") else "❌ No",
            }
        ]
    except Exception as e:
        return [{"platform": "Twitter", "error": str(e)}]


# Load Twitter API key from API_KEY folder (optional)
TWITTER_API_KEY = None
try:
    with open("API_KEY/twitter_api_key.txt", "r") as f:
        TWITTER_API_KEY = f.read().strip()
except FileNotFoundError:
    TWITTER_API_KEY = None


# Snapchat check function
def check_snapchat(username):
    url = f"https://www.snapchat.com/add/{username}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            return [{"platform": "Snapchat", "error": "No profile found"}]
        soup = BeautifulSoup(res.text, "html.parser")
        og_title = soup.find("meta", property="og:title")
        og_desc = soup.find("meta", property="og:description")
        og_image = soup.find("meta", property="og:image")

        if not og_title or "Snapchat" not in og_title.get("content", ""):
            return [{"platform": "Snapchat", "error": "No profile found"}]

        return [
            {
                "platform": "Snapchat",
                "username": username,
                "display_name": og_title.get("content", ""),
                "bio": og_desc.get("content", ""),
                "profile_url": url,
                "avatar": og_image.get("content", ""),
                "verified": "❌ No",  # No easy way to detect verification yet
            }
        ]
    except Exception as e:
        return [{"platform": "Snapchat", "error": str(e)}]


# Generate HTML report after the scan
def generate_html_report(results, username):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"handlehawk_report_{username}_{now}.html"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HandleHawk Report - {username}</title>
    <style>
        body {{ font-family: monospace; background: #0f0f0f; color: #f0f0f0; padding: 20px; }}
        .platform {{ margin-bottom: 20px; border-bottom: 1px solid #555; padding-bottom: 10px; }}
        img {{ max-height: 100px; border-radius: 10px; }}
        a {{ color: #6cf; }}
        .error {{ color: orange; }}
    </style>
</head>
<body>
<h1>🔎 HandleHawk Report</h1>
<h2>Username Checked: {username}</h2>
<p>Generated on: {now}</p>
"""

    for result in results:
        html += f"<div class='platform'>\n<h3>{result['platform']}</h3>\n"

        # Custom PayPal rendering
        if result["platform"] == "PayPal":
            html += "<ul>"
            for key in ["full_name", "first_name", "last_name", "bio", "currency"]:
                if result.get(key):
                    html += f"<li><strong>{key.replace('_', ' ').title()}:</strong> {result[key]}</li>"
            if result.get("avatar"):
                html += f"<li><img src='{result['avatar']}' alt='Profile Photo'></li>"
            if result.get("profile_url"):
                html += f"<li><a href='{result['profile_url']}' target='_blank'>{result['profile_url']}</a></li>"
            html += "</ul>\n</div>\n"
            continue  # Skip default rendering

        # Default rendering
        if "error" in result:
            html += f"<p class='error'>No profile found</p>\n"
        else:
            for key, label in [
                ("handle", "Handle"),
                ("display_name", "Display Name"),
                ("name", "Name"),
                ("username", "Username"),
                ("acct", "Account"),
                ("about", "About"),
                ("bio", "Bio"),
                ("created_at", "Created"),
                ("followers", "Followers"),
                ("following", "Following"),
                ("posts", "Posts"),
                ("total_karma", "Total Karma"),
                ("link_karma", "Link Karma"),
                ("comment_karma", "Comment Karma"),
                ("website", "Website"),
                ("verified", "Verified"),
            ]:
                if result.get(key):
                    html += f"<p><strong>{label}:</strong> {result[key]}</p>\n"
            if result.get("profile_url"):
                html += f"<p><strong>Profile Link:</strong> <a href='{result['profile_url']}' target='_blank'>{result['profile_url']}</a></p>\n"
            if result.get("avatar"):
                html += f"<p><img src='{result['avatar']}' alt='Avatar'></p>\n"
            if result.get("banner"):
                html += f"<p><img src='{result['banner']}' alt='Banner'></p>\n"
        html += "</div>\n"

    html += "</body></html>"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ HTML report saved as: {filename}")


if __name__ == "__main__":
    username = input("Enter a username to scan: ").strip()
    all_results = []

    checks = [
        ("Bluesky", check_bluesky),
        ("Nostr", check_nostr),
        ("Mastodon", check_mastodon),
        ("TruthSocial", check_truthsocial),
        ("Reddit", check_reddit),
        ("Snapchat", check_snapchat),
        ("PayPal", paypal.check_paypal),
    ]

    if TWITTER_API_KEY:
        checks.append(("Twitter", lambda u: check_twitter_via_api(u, TWITTER_API_KEY)))
    else:
        print("⚠️  No Twitter API key found. Skipping Twitter check.")

    # Perform all checks
    for name, func in checks:
        spinner = Spinner(f"Checking {name}")
        spinner.start()
        try:
            result = func(username)
            if result and "error" not in result[0]:
                all_results += result
            else:
                all_results.append({"platform": name, "error": "No profile found"})
        except Exception as e:
            all_results.append({"platform": name, "error": f"Error: {str(e)}"})
        spinner.stop()

    # Generate report and print summary
    generate_html_report(all_results, username)

    print("\n🔍 Summary:")
    for result in all_results:
        platform = result.get("platform", "Unknown")
        if "error" in result:
            print(f"🔍 {platform}: No profile found")
        else:
            name = (
                result.get("display_name")
                or result.get("name")
                or result.get("username")
            )
            url = result.get("profile_url", "(no link)")
            print(f"✅ {platform}: Found profile {name} → {url}")
