# 🔍 DORKBOY
### Professional Google Dorking Framework | Bug Bounty Edition

```
  ██████╗  ██████╗ ██████╗ ██╗  ██╗██████╗  ██████╗ ██╗   ██╗
  ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔═══██╗╚██╗ ██╔╝
  ██║  ██║██║   ██║██████╔╝█████╔╝ ██████╔╝██║   ██║ ╚████╔╝ 
  ██║  ██║██║   ██║██╔══██╗██╔═██╗ ██╔══██╗██║   ██║  ╚██╔╝  
  ██████╔╝╚██████╔╝██║  ██║██║  ██╗██████╔╝╚██████╔╝   ██║   
  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝   ╚═╝   
```

![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.0.0-orange?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Linux%20|%20Windows%20|%20macOS-lightgrey?style=flat-square)

A powerful CLI-based Google Dorking tool for passive recon during bug bounty hunting. Dorkboy comes loaded with **129+ handcrafted dorks** across **9 categories**, severity-tagged and ready to fire in your browser — all for authorized recon only.

---

## ✨ Features

- 🎯 **129+ curated dorks** across 9 categories
- 🔴 Severity-tagged dorks (P1 / P2) for prioritized hunting
- 🌐 Opens dorks directly in browser (Google Search)
- 🔍 Keyword search across all dorks
- 📋 Dump all dorks for any target at once
- 🎨 Rich color-coded terminal UI (falls back gracefully if `rich` not installed)
- 🔄 Change target anytime mid-session
- 💻 Works on Linux, Windows, macOS

---

## 📂 Dork Categories

| # | Category | Description |
|---|----------|-------------|
| 1 | 🔴 PII & Personal Data | Emails, SSNs, DOBs, passports in exposed files |
| 2 | 🔑 Credentials & Secrets | API keys, AWS creds, .env files, DB passwords |
| 3 | 📄 Sensitive Files | .sql, .bak, .env, .pem, .yaml config files |
| 4 | 📁 Open Directories | Directory listings, backup dirs, admin dirs |
| 5 | 🛡️ Admin & Login Panels | phpMyAdmin, cPanel, wp-admin, dashboards |
| 6 | 🔌 API & Endpoints | Swagger, GraphQL, REST API docs |
| 7 | 🖥️ Server & Tech Info | Error pages, server banners, tech stack leaks |
| 8 | ☁️ Cloud & Storage | S3 buckets, Azure blobs, GCP storage |
| 9 | 🐛 Vulnerability Patterns | SQLi errors, LFI patterns, debug pages |

---

## 🚀 Installation

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/dorkboy.git
cd dorkboy
```

### 2. Install dependencies
```bash
pip install rich
```
> `rich` is optional — Dorkboy works without it, but the colors and UI look much better with it.

### 3. Run it
```bash
python dorkboy.py
```

---

## 🖥️ Usage

```
Enter your target domain when prompted:
  dorkboy@target> ❯ example.com

Then choose from the menu:
  [1-9]  Browse a dork category
  [A]    Dump ALL dorks for target
  [S]    Search dorks by keyword
  [T]    Change target domain
  [Q]    Quit
```

---

## ⚠️ Legal Disclaimer

> **This tool is for educational purposes and authorized security testing ONLY.**  
> Using Google dorks against targets you don't have permission to test may violate laws including the Computer Fraud and Abuse Act (CFAA) and similar legislation in your country.  
> **The author is not responsible for any misuse of this tool.**  
> Always get written permission before testing any target.

---

## 🤝 Contributing

Pull requests are welcome! If you have new dork ideas or category suggestions, feel free to open an issue or PR.

1. Fork the repo
2. Create your branch: `git checkout -b feature/new-dorks`
3. Commit changes: `git commit -m "Add new cloud dorks"`
4. Push: `git push origin feature/new-dorks`
5. Open a Pull Request

---

## 👤 Author

**Anurag Sunil**  
Cybersecurity Enthusiast | Bug Bounty Hunter  
🔗 [GitHub](https://github.com/anuragsunil03)

---

