# 🦅 HandleHawk

**HandleHawk** is a cross-platform username reconnaissance tool for OSINT analysts, CyberSecurity professionnals, Red Teamers, and CTF enthusiasts. 
It scans multiple social platforms to gather publicly available user information by just a single username input.

> **"Find the signal in the noise."**

<p align="center">
  <img src="Assets/HandleHawk_Logo.png" alt="HandleHawk Logo" width="733">
</p>




# 📁 Repository Structure



```
HandleHawk/
│
├── API_KEY/
│   └── twitter_api_key.txt      # Optional Twitter API Key file
│
├── handlehawk.py                # Main script
├── requirements.txt             # Python dependencies
├── README.md                    # Tool documentation
├── Assets/                      # Assets folder
    └── HandleHawk_Logo.png      # HandleHawk logo
    └── Report_Sample.html       # HandleHawk report sample
```

---

## 🚀 Features

- 🔍 Scans multiple platforms:
  - Bluesky
  - Mastodon
  - Nostr
  - TruthSocial
  - Reddit
  - Snapchat
  - Twitter (via optional RapidAPI)
- 🛡️ Resilient to Cloudflare thanks to cloudscraper
- 📄 Generates a clean, dark-mode HTML report
- 🧠 Smart spinner for each check (UX-friendly)
- 🔐 Optional Twitter API key (kept local)

---

## 📦 Installation

```bash
git clone https://github.com/C3n7ral051nt4g3ncy/HandleHawk.git
cd HandleHawk
pip install -r requirements.txt
```

---

# 🔑 Twitter API Key (Optional)

**To enable Twitter checks (via RapidAPI), do the following:**

- Create a free account on [Rapid API](https://rapidapi.com/)
- Choose the [free Twitter API plan](https://rapidapi.com/alexanderxbx/api/twitter-api45) (1000 requests per month) by **Alexander Vikhorev**
- Paste your API key into the file `twitter_api_key.txt`
- **If no key is found, HandleHawk will skip X/Twitter and continue without errors**

---

# ⚙️ Usage
Run the tool from terminal:

```bash
python3 handlehawk.py
```


---
## 🛣️ Roadmap

A list of upcoming features and improvements planned for **HandleHawk**:

### ✅ v1.0 (Completed)
- [x] Core recon engine with spinner animations  
- [x] Cross-platform username scanning for:
  - [x] Reddit  
  - [x] Mastodon  
  - [x] Bluesky  
  - [x] TruthSocial  
  - [x] Nostr  
- [x] Twitter (X) scanning via optional RapidAPI key  
- [x] HTML report generator with profile summaries & images which does more than other username enumeration tools
- [x] Optional `API_KEY/` folder for key management  
- [x] User-agent spoofing & anti-bot headers  

---

### 🧠 Planned for v1.1
  
- [ ] CSV report export  
- [ ] JSON output for automation
- [ ] Support for more platforms:
  - [ ] Threads
  - [ ] Facebook
  - [ ] Telegram  
  - [ ] LinkedIn
  - [ ] YouTube  

---

# 👨‍💻 Author

Developed by [C3n7ral051nt4g3ncy](https://github.com/C3n7ral051nt4g3ncy)

---

# 💡 Suggestions?

- Open an issue or start a discussion! Contributions and feature ideas are welcome 🦅
- If you use HandleHawk in your investigations, feel free to give a ⭐️ or suggest a feature!























