#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║                        D O R K B O Y                            ║
║              Professional Google Dorking Framework              ║
║                   Bug Bounty Recon Edition                      ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import webbrowser
import urllib.parse
import platform

# ── Try rich for colors, fallback to plain ──────────────────────────
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.columns import Columns
    from rich import box
    from rich.prompt import Prompt
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.align import Align
    from rich.rule import Rule
    from rich.style import Style
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False

# ══════════════════════════════════════════════════════════════════
#  ASCII ART & BRANDING
# ══════════════════════════════════════════════════════════════════

BANNER = r"""
  ██████╗  ██████╗ ██████╗ ██╗  ██╗██████╗  ██████╗ ██╗   ██╗
  ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔═══██╗╚██╗ ██╔╝
  ██║  ██║██║   ██║██████╔╝█████╔╝ ██████╔╝██║   ██║ ╚████╔╝ 
  ██║  ██║██║   ██║██╔══██╗██╔═██╗ ██╔══██╗██║   ██║  ╚██╔╝  
  ██████╔╝╚██████╔╝██║  ██║██║  ██╗██████╔╝╚██████╔╝   ██║   
  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝   ╚═╝   
"""

TAGLINE = "[ Professional Google Dorking Framework | Bug Bounty Edition ]"
VERSION = "v1.0.0"
AUTHOR  = "Passive Recon Tool | For Authorized Testing Only"

SEP = "═" * 68

# ══════════════════════════════════════════════════════════════════
#  DORK DATABASE
# ══════════════════════════════════════════════════════════════════

CATEGORIES = {
    "1": {
        "name": "PII & Personal Data",
        "icon": "[PII]",
        "color": "bright_red",
        "dorks": [
            ("P1", "site:{T} ext:csv intext:\"email\"",                        "CSV files with email addresses"),
            ("P1", "site:{T} ext:xls intext:\"ssn\" OR intext:\"social security\"", "SSN in spreadsheets"),
            ("P1", "site:{T} ext:sql intext:\"INSERT INTO\" intext:\"email\"",  "SQL dumps with user emails"),
            ("P1", "site:{T} intext:\"@gmail.com\" OR intext:\"@yahoo.com\" ext:txt", "Email lists in text files"),
            ("P1", "site:{T} intext:\"date of birth\" OR intext:\"dob\" ext:csv", "DOB in exported files"),
            ("P1", "site:{T} intext:\"phone number\" ext:xls OR ext:csv",       "Phone numbers in files"),
            ("P1", "site:{T} intext:\"passport\" OR intext:\"national id\" ext:pdf", "Passport/ID documents"),
            ("P1", "site:{T} intext:\"credit card\" OR intext:\"card number\" ext:log", "CC data in logs"),
            ("P2", "site:{T} intext:\"address\" intext:\"zip\" ext:csv OR ext:xls", "Physical address exports"),
            ("P2", "site:{T} intext:\"full name\" intext:\"email\" ext:json",   "PII in JSON responses"),
            ("P1", "site:{T} intext:\"gender\" intext:\"age\" intext:\"email\" ext:csv", "Demographic data dump"),
            ("P1", "site:{T} filetype:sql intext:\"users\" intext:\"password\"","SQL user table dump"),
        ],
    },
    "2": {
        "name": "Credentials & Secrets",
        "icon": "[KEY]",
        "color": "bright_yellow",
        "dorks": [
            ("P1", "site:{T} intext:\"api_key\" OR intext:\"apikey\" OR intext:\"api-key\"", "Exposed API keys"),
            ("P1", "site:{T} intext:\"secret_key\" OR intext:\"client_secret\"","Secret keys exposed"),
            ("P1", "site:{T} intext:\"password\" ext:log OR ext:txt OR ext:conf","Passwords in logs/configs"),
            ("P1", "site:{T} intext:\"BEGIN RSA PRIVATE KEY\"",                 "RSA private key exposed"),
            ("P1", "site:{T} intext:\"Authorization: Bearer\"",                 "Bearer tokens in pages"),
            ("P1", "site:{T} intext:\"aws_access_key_id\"",                    "AWS credentials"),
            ("P1", "site:{T} intext:\"AKIA\" intext:\"secret\"",               "AWS IAM keys"),
            ("P1", "site:{T} intext:\"db_password\" OR intext:\"DB_PASS\"",    "DB password exposure"),
            ("P2", "site:{T} intext:\"smtp_password\" OR intext:\"mail_pass\"", "SMTP credentials"),
            ("P1", "site:{T} intext:\"private_key\" ext:json OR ext:env",      "Private keys in config"),
            ("P1", "site:{T} inurl:\".env\" intext:\"password\"",              ".env file with credentials"),
            ("P1", "site:{T} intext:\"connectionString\" intext:\"password\"",  "DB connection strings"),
            ("P1", "site:{T} ext:env intext:\"SECRET\"",                       "Secret in env files"),
            ("P1", "site:{T} intext:\"token\" intext:\"secret\" ext:json",     "Token secrets in JSON"),
        ],
    },
    "3": {
        "name": "Sensitive Files",
        "icon": "[FILE]",
        "color": "bright_magenta",
        "dorks": [
            ("P1", "site:{T} ext:env",                                          "Environment config files"),
            ("P2", "site:{T} ext:bak OR ext:backup OR ext:old",                "Backup files"),
            ("P2", "site:{T} ext:conf OR ext:config",                          "Configuration files"),
            ("P1", "site:{T} ext:sql",                                          "SQL database dumps"),
            ("P2", "site:{T} ext:log",                                          "Log files"),
            ("P1", "site:{T} ext:key OR ext:pem",                              "Key/certificate files"),
            ("P1", "site:{T} ext:yaml OR ext:yml intext:\"password\"",         "YAML files with creds"),
            ("P2", "site:{T} ext:ini intext:\"password\"",                     "INI config with passwords"),
            ("P1", "site:{T} inurl:wp-config.php",                             "WordPress config exposed"),
            ("P1", "site:{T} inurl:config.php intext:\"password\"",            "PHP config with passwords"),
            ("P1", "site:{T} ext:py intext:\"password\" OR intext:\"secret\"", "Python files with secrets"),
            ("P1", "site:{T} inurl:\".git\" intitle:\"index of\"",             "Git repo exposed"),
            ("P2", "site:{T} ext:xml inurl:config",                            "XML config files"),
            ("P2", "site:{T} ext:sh inurl:backup",                             "Backup shell scripts"),
        ],
    },
    "4": {
        "name": "Open Directories",
        "icon": "[DIR]",
        "color": "bright_cyan",
        "dorks": [
            ("P2", "site:{T} intitle:\"index of\"",                            "Generic directory listing"),
            ("P2", "site:{T} intitle:\"index of\" \"parent directory\"",       "Open parent directory"),
            ("P1", "site:{T} intitle:\"index of\" inurl:/backup",              "Backup dir exposed"),
            ("P2", "site:{T} intitle:\"index of\" inurl:/uploads",             "Upload directory open"),
            ("P1", "site:{T} intitle:\"index of\" inurl:/admin",               "Admin dir listing"),
            ("P2", "site:{T} intitle:\"index of\" inurl:/logs",                "Logs directory open"),
            ("P1", "site:{T} intitle:\"index of\" inurl:/database",            "Database dir exposed"),
            ("P1", "site:{T} intitle:\"index of\" inurl:/private",             "Private dir listing"),
            ("P1", "site:{T} intitle:\"index of\" inurl:/config",              "Config dir exposed"),
            ("P2", "site:{T} intitle:\"index of\" ext:pdf",                    "PDF directory listing"),
        ],
    },
    "5": {
        "name": "Admin & Login Panels",
        "icon": "[ADM]",
        "color": "bright_green",
        "dorks": [
            ("P2", "site:{T} inurl:admin",                                      "Admin panel URL"),
            ("P2", "site:{T} inurl:login inurl:admin",                         "Admin login page"),
            ("P2", "site:{T} intitle:\"admin\" inurl:login",                   "Admin login title"),
            ("P1", "site:{T} inurl:phpmyadmin",                                "phpMyAdmin exposed"),
            ("P2", "site:{T} inurl:cpanel",                                    "cPanel access"),
            ("P2", "site:{T} inurl:wp-admin",                                  "WordPress admin panel"),
            ("P2", "site:{T} inurl:dashboard",                                 "Dashboard pages"),
            ("P2", "site:{T} inurl:portal",                                    "Employee/user portals"),
            ("P2", "site:{T} inurl:webmail",                                   "Webmail interface"),
            ("P2", "site:{T} inurl:control-panel",                             "Control panel page"),
            ("P2", "site:{T} inurl:admin/login.php",                           "PHP admin login"),
            ("P2", "site:{T} inurl:/manage",                                   "Management interface"),
        ],
    },
    "6": {
        "name": "API & Endpoints",
        "icon": "[API]",
        "color": "bright_blue",
        "dorks": [
            ("P2", "site:{T} inurl:/api/v1",                                   "API v1 endpoints"),
            ("P2", "site:{T} inurl:/api/v2",                                   "API v2 endpoints"),
            ("P2", "site:{T} inurl:/graphql",                                  "GraphQL endpoint"),
            ("P2", "site:{T} inurl:/swagger",                                  "Swagger API docs"),
            ("P2", "site:{T} inurl:swagger-ui.html",                           "Swagger UI exposed"),
            ("P2", "site:{T} inurl:/api-docs",                                 "API documentation"),
            ("P1", "site:{T} inurl:/actuator",                                 "Spring actuator exposed"),
            ("P2", "site:{T} inurl:/metrics",                                  "Metrics endpoint"),
            ("P2", "site:{T} ext:json inurl:/api",                             "JSON API responses"),
            ("P2", "site:{T} inurl:/rest/api",                                 "REST API endpoint"),
            ("P2", "site:{T} inurl:/.well-known",                              "Well-known metadata"),
        ],
    },
    "7": {
        "name": "Subdomains & Infrastructure",
        "icon": "[SUB]",
        "color": "cyan",
        "dorks": [
            ("INFO","site:*.{T}",                                               "All indexed subdomains"),
            ("INFO","site:*.{T} -www",                                         "Non-www subdomains"),
            ("P2", "site:*.{T} inurl:dev OR inurl:develop",                    "Dev subdomains"),
            ("P2", "site:*.{T} inurl:staging",                                 "Staging environment"),
            ("P2", "site:*.{T} inurl:test OR inurl:testing",                   "Test environment"),
            ("P2", "site:*.{T} inurl:uat",                                     "UAT environment"),
            ("P1", "site:*.{T} inurl:internal OR inurl:intranet",              "Internal systems"),
            ("P2", "site:*.{T} inurl:jenkins OR inurl:ci",                     "CI/CD systems"),
            ("P1", "site:*.{T} inurl:kibana OR inurl:elastic",                 "Logging systems exposed"),
            ("P2", "site:*.{T} inurl:jira OR inurl:confluence",                "Project management"),
            ("P2", "site:*.{T} inurl:vpn",                                     "VPN portal"),
        ],
    },
    "8": {
        "name": "Error & Debug Info",
        "icon": "[ERR]",
        "color": "red",
        "dorks": [
            ("P1", "site:{T} intext:\"SQL syntax\" OR intext:\"mysql_fetch\"", "MySQL error exposure"),
            ("P1", "site:{T} intext:\"ORA-01756\" OR intext:\"Oracle\"",       "Oracle DB errors"),
            ("P2", "site:{T} intext:\"Traceback (most recent call last)\"",    "Python stack trace"),
            ("P2", "site:{T} intext:\"stack trace\" intext:\"at line\"",       "Stack trace exposure"),
            ("P2", "site:{T} intext:\"Warning: include\" OR intext:\"Warning: require\"", "PHP include warnings"),
            ("P2", "site:{T} intext:\"Fatal error:\" intext:\".php\"",         "PHP fatal errors"),
            ("P1", "site:{T} intext:\"Warning: mysql_connect()\"",             "MySQL connect warning"),
            ("P2", "site:{T} intext:\"JDBC Exception\" OR intext:\"Hibernate\"","Java DB errors"),
            ("P3", "site:{T} intitle:\"500 Internal Server Error\"",           "500 error pages"),
            ("P3", "site:{T} intitle:\"403 Forbidden\"",                       "403 restricted pages"),
        ],
    },
    "9": {
        "name": "Cloud & Storage",
        "icon": "[CLD]",
        "color": "yellow",
        "dorks": [
            ("P1", "site:{T} inurl:s3.amazonaws.com",                          "S3 bucket links"),
            ("P1", "site:{T} intext:\"s3.amazonaws.com\" ext:html OR ext:xml", "S3 references in pages"),
            ("P1", "site:{T} inurl:blob.core.windows.net",                     "Azure Blob Storage"),
            ("P1", "site:{T} inurl:storage.googleapis.com",                    "GCS bucket exposed"),
            ("P1", "site:{T} intext:\"AWSSecretKey\" OR intext:\"AWSAccessKeyId\"", "AWS creds in pages"),
            ("P1", "site:{T} intext:\"firebase\" intext:\"apiKey\"",           "Firebase config exposed"),
            ("P2", "site:{T} inurl:digitaloceanspaces.com",                    "DigitalOcean Spaces"),
            ("P2", "site:{T} intext:\"heroku\" intext:\"postgres\"",           "Heroku DB config"),
        ],
    },
    "10": {
        "name": "Source Code Leaks",
        "icon": "[SRC]",
        "color": "magenta",
        "dorks": [
            ("P1", "site:{T} inurl:/.git/config",                              "Git config exposed"),
            ("P1", "site:{T} inurl:/.svn/entries",                             "SVN repo exposed"),
            ("P1", "site:{T} ext:js intext:\"api_key\" OR intext:\"apiKey\"",  "API keys in JS"),
            ("P1", "site:{T} ext:js intext:\"secret\" OR intext:\"password\"", "Secrets in JS files"),
            ("P1", "site:{T} ext:php intext:\"eval(\" intext:\"base64\"",      "Obfuscated PHP (webshell?)"),
            ("P2", "site:{T} inurl:debug=true OR inurl:debug=1",               "Debug mode enabled"),
            ("P2", "site:{T} inurl:test.php OR inurl:info.php",                "Test files live in prod"),
            ("P2", "site:{T} ext:js intext:\"token\"",                         "Tokens in JavaScript"),
            ("P2", "site:{T} inurl:index.php?id=",                             "SQLi prone URLs"),
        ],
    },
    "11": {
        "name": "Info Disclosure",
        "icon": "[INF]",
        "color": "green",
        "dorks": [
            ("INFO","site:{T} inurl:robots.txt",                               "Robots.txt reveals hidden paths"),
            ("INFO","site:{T} inurl:sitemap.xml",                              "Sitemap for all URLs"),
            ("P2", "site:{T} inurl:phpinfo.php",                               "PHP info page"),
            ("P2", "site:{T} inurl:server-status",                             "Apache server-status"),
            ("P2", "site:{T} inurl:server-info",                               "Apache server-info"),
            ("P2", "site:{T} inurl:.htaccess",                                 "htaccess file exposed"),
            ("P3", "site:{T} inurl:crossdomain.xml",                           "Flash crossdomain policy"),
            ("P3", "site:{T} inurl:package.json",                              "NPM package config"),
            ("P3", "site:{T} inurl:composer.json",                             "PHP composer config"),
            ("INFO","site:{T} inurl:security.txt",                             "Security contact info"),
            ("INFO","site:{T} inurl:CHANGELOG",                                "Version changelogs"),
        ],
    },
    "12": {
        "name": "Network & Devices",
        "icon": "[NET]",
        "color": "bright_white",
        "dorks": [
            ("P2", "site:{T} intitle:\"Network Camera\" OR intitle:\"webcam\"","Exposed webcams"),
            ("P1", "site:{T} intitle:\"SCADA\" OR intitle:\"HMI\"",           "Industrial control systems"),
            ("P2", "site:{T} intitle:\"Router\" intext:\"login\"",             "Router login pages"),
            ("P2", "site:{T} intitle:\"VPN\" inurl:login",                    "VPN login pages"),
            ("P2", "site:{T} intitle:\"VMware\" OR intitle:\"ESXi\"",         "VMware interfaces"),
            ("P2", "site:{T} intitle:\"Kibana\" OR intitle:\"Grafana\"",      "Monitoring dashboards"),
            ("P3", "site:{T} inurl:8080 OR inurl:8443 OR inurl:8888",         "Alt port services"),
        ],
    },
}

SEV_COLOR = {"P1": "\033[91m", "P2": "\033[93m", "P3": "\033[92m", "INFO": "\033[90m"}
SEV_RICH  = {"P1": "bold red", "P2": "bold yellow", "P3": "bold green", "INFO": "dim white"}
RESET     = "\033[0m"
BOLD      = "\033[1m"
GREEN     = "\033[92m"
CYAN      = "\033[96m"
RED       = "\033[91m"
YELLOW    = "\033[93m"
MAGENTA   = "\033[95m"
DIM       = "\033[2m"
BLUE      = "\033[94m"

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════

def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

def pause():
    input(f"\n{DIM}  Press Enter to continue...{RESET}")

def resolve(dork, target):
    return dork.replace("{T}", target)

def google_url(dork, target):
    q = resolve(dork, target)
    return f"https://www.google.com/search?q={urllib.parse.quote(q)}"

def open_in_browser(dork, target):
    webbrowser.open(google_url(dork, target))

def sev_badge(sev):
    c = SEV_COLOR.get(sev, "")
    return f"{c}[{sev}]{RESET}"

def count_by_sev():
    counts = {"P1": 0, "P2": 0, "P3": 0, "INFO": 0}
    for cat in CATEGORIES.values():
        for sev, _, _ in cat["dorks"]:
            counts[sev] = counts.get(sev, 0) + 1
    return counts

def total_dorks():
    return sum(len(c["dorks"]) for c in CATEGORIES.values())

# ══════════════════════════════════════════════════════════════════
#  DISPLAY FUNCTIONS (plain terminal)
# ══════════════════════════════════════════════════════════════════

def print_banner():
    clear()
    print(f"{GREEN}{BANNER}{RESET}")
    print(f"{CYAN}  {TAGLINE}{RESET}")
    print(f"{DIM}  {VERSION}  ·  {AUTHOR}{RESET}")
    print(f"\n{DIM}  {SEP}{RESET}\n")

def print_stats(target):
    counts = count_by_sev()
    total  = total_dorks()
    cats   = len(CATEGORIES)
    print(f"  {BOLD}TARGET :{RESET} {GREEN}{target}{RESET}")
    print(f"  {BOLD}DORKS  :{RESET} {CYAN}{total}{RESET} across {CYAN}{cats}{RESET} categories")
    print(f"  {RED}[P1]{RESET} {counts['P1']}  "
          f"{YELLOW}[P2]{RESET} {counts['P2']}  "
          f"{GREEN}[P3]{RESET} {counts['P3']}  "
          f"{DIM}[INFO]{RESET} {counts['INFO']}")
    print(f"\n{DIM}  {SEP}{RESET}\n")

def print_menu(target):
    print_banner()
    print_stats(target)
    print(f"  {BOLD}{CYAN}[ CATEGORIES ]{RESET}\n")
    for k, v in CATEGORIES.items():
        p1 = sum(1 for s, _, _ in v["dorks"] if s == "P1")
        badge = f"{RED} ★{p1}×P1{RESET}" if p1 else ""
        icon  = v["icon"]
        name  = v["name"]
        count = len(v["dorks"])
        print(f"  {DIM}[{k:>2}]{RESET}  {YELLOW}{icon}{RESET}  {BOLD}{name:<30}{RESET}  {DIM}{count} dorks{RESET}{badge}")
    print()
    print(f"  {DIM}[ A ]{RESET}  {MAGENTA}[ALL]{RESET}  {BOLD}{'Dump ALL dorks for target':<30}{RESET}  {DIM}{total_dorks()} dorks{RESET}")
    print(f"  {DIM}[ S ]{RESET}  {CYAN}[SCH]{RESET}  {BOLD}{'Search across all dorks':<30}{RESET}")
    print(f"  {DIM}[ T ]{RESET}  {GREEN}[TGT]{RESET}  {BOLD}{'Change target domain':<30}{RESET}  {DIM}current: {target}{RESET}")
    print(f"  {DIM}[ Q ]{RESET}  {RED}[EXT]{RESET}  {BOLD}{'Quit Dorkboy':<30}{RESET}")
    print(f"\n{DIM}  {SEP}{RESET}")

def print_dork_list(cat_key, target):
    cat = CATEGORIES[cat_key]
    clear()
    print(f"\n{GREEN}{BANNER}{RESET}")
    print(f"  {BOLD}{CYAN}{cat['icon']} {cat['name']}{RESET}  ─  {DIM}{len(cat['dorks'])} dorks  ·  target: {GREEN}{target}{RESET}")
    print(f"\n{DIM}  {SEP}{RESET}\n")

    for i, (sev, dork, note) in enumerate(cat["dorks"], 1):
        resolved = resolve(dork, target)
        badge    = sev_badge(sev)
        print(f"  {DIM}[{i:>2}]{RESET} {badge}  {CYAN}{resolved}{RESET}")
        print(f"        {DIM}↳ {note}{RESET}\n")

    print(f"{DIM}  {SEP}{RESET}")
    print(f"\n  {BOLD}Actions:{RESET}")
    print(f"  {DIM}[number]{RESET} Open dork in browser")
    print(f"  {DIM}[  A  ]{RESET} Open ALL in browser")
    print(f"  {DIM}[  C  ]{RESET} Copy all dorks to clipboard (print to screen)")
    print(f"  {DIM}[  B  ]{RESET} Back to main menu")
    print(f"\n{DIM}  {SEP}{RESET}")

    while True:
        choice = input(f"\n  {GREEN}dorkboy{RESET}{DIM}@{RESET}{GREEN}{target}{RESET} {YELLOW}❯{RESET} ").strip().upper()
        if choice == "B":
            break
        elif choice == "A":
            print(f"\n  {YELLOW}Opening {len(cat['dorks'])} dorks in browser...{RESET}")
            for _, d, _ in cat["dorks"]:
                open_in_browser(d, target)
                time.sleep(0.4)
            print(f"  {GREEN}✓ Done!{RESET}")
            pause()
            break
        elif choice == "C":
            print(f"\n{DIM}  ── All dorks for {target} ──{RESET}")
            for _, d, _ in cat["dorks"]:
                print(f"  {resolve(d, target)}")
            print(f"{DIM}  ── End ──{RESET}")
            pause()
            break
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(cat["dorks"]):
                _, d, note = cat["dorks"][idx]
                url = google_url(d, target)
                print(f"\n  {DIM}Opening:{RESET} {CYAN}{resolve(d, target)}{RESET}")
                open_in_browser(d, target)
                print(f"  {GREEN}✓ Launched in browser{RESET}")
            else:
                print(f"  {RED}Invalid number{RESET}")
        else:
            print(f"  {RED}Unknown command{RESET}")

def dump_all(target):
    clear()
    print(f"\n{GREEN}{BANNER}{RESET}")
    print(f"  {BOLD}{MAGENTA}[ALL]{RESET}  Complete Dork Dump  ·  target: {GREEN}{target}{RESET}")
    print(f"\n{DIM}  {SEP}{RESET}\n")
    total = 0
    for k, cat in CATEGORIES.items():
        print(f"  {YELLOW}{cat['icon']} {cat['name']}{RESET}")
        for sev, dork, note in cat["dorks"]:
            resolved = resolve(dork, target)
            badge    = sev_badge(sev)
            print(f"    {badge}  {CYAN}{resolved}{RESET}")
            print(f"           {DIM}↳ {note}{RESET}")
            total += 1
        print()
    print(f"{DIM}  {SEP}{RESET}")
    print(f"\n  {GREEN}✓ {total} dorks listed for {target}{RESET}")
    print(f"\n  {BOLD}Actions:{RESET}")
    print(f"  {DIM}[  O  ]{RESET} Open ALL {total} dorks in browser (bulk)")
    print(f"  {DIM}[  B  ]{RESET} Back to menu")

    while True:
        choice = input(f"\n  {GREEN}dorkboy{RESET}{DIM}@{RESET}{GREEN}{target}{RESET} {YELLOW}❯{RESET} ").strip().upper()
        if choice == "B":
            break
        elif choice == "O":
            print(f"\n  {YELLOW}Opening {total} dorks in browser... (this may take a while){RESET}")
            for cat in CATEGORIES.values():
                for _, d, _ in cat["dorks"]:
                    open_in_browser(d, target)
                    time.sleep(0.35)
            print(f"  {GREEN}✓ All dorks launched!{RESET}")
            pause()
            break
        else:
            print(f"  {RED}Unknown command. [O] open all  [B] back{RESET}")

def search_dorks(target):
    clear()
    print(f"\n{GREEN}{BANNER}{RESET}")
    print(f"  {BOLD}{CYAN}[SEARCH]{RESET}  Search across all {total_dorks()} dorks")
    print(f"\n{DIM}  {SEP}{RESET}\n")
    kw = input(f"  {YELLOW}Enter keyword:{RESET} ").strip().lower()
    if not kw:
        return

    results = []
    for cat in CATEGORIES.values():
        for sev, dork, note in cat["dorks"]:
            resolved = resolve(dork, target)
            if kw in resolved.lower() or kw in note.lower():
                results.append((sev, dork, note, cat["name"]))

    print(f"\n{DIM}  {SEP}{RESET}")
    print(f"  {GREEN}{len(results)}{RESET} results for \"{BOLD}{kw}{RESET}\"\n")

    if not results:
        print(f"  {RED}No dorks matched.{RESET}")
        pause()
        return

    for i, (sev, dork, note, catname) in enumerate(results, 1):
        badge    = sev_badge(sev)
        resolved = resolve(dork, target)
        print(f"  {DIM}[{i:>2}]{RESET} {badge}  {CYAN}{resolved}{RESET}")
        print(f"        {DIM}↳ {note}  [{catname}]{RESET}\n")

    print(f"{DIM}  {SEP}{RESET}")
    print(f"  {DIM}[number]{RESET} Open in browser   {DIM}[B]{RESET} Back")

    while True:
        choice = input(f"\n  {GREEN}dorkboy{RESET}{DIM}@search>{RESET} {YELLOW}❯{RESET} ").strip().upper()
        if choice == "B":
            break
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(results):
                sev, d, note, _ = results[idx]
                open_in_browser(d, target)
                print(f"  {GREEN}✓ Launched in browser{RESET}")
            else:
                print(f"  {RED}Invalid number{RESET}")
        else:
            print(f"  {RED}Unknown command{RESET}")

# ══════════════════════════════════════════════════════════════════
#  MAIN LOOP
# ══════════════════════════════════════════════════════════════════

def main():
    # Startup animation
    clear()
    print(f"\n{GREEN}", end="", flush=True)
    for line in BANNER.split("\n"):
        print(line)
        time.sleep(0.05)
    print(f"{RESET}")
    time.sleep(0.3)
    print(f"  {CYAN}Initializing DORKBOY...{RESET}")
    time.sleep(0.2)
    print(f"  {DIM}Loading {total_dorks()} dorks across {len(CATEGORIES)} categories...{RESET}")
    time.sleep(0.4)
    print(f"  {GREEN}✓ Ready.{RESET}\n")
    time.sleep(0.4)

    # Always ask for target on launch
    print(f"  {DIM}{SEP}{RESET}")
    print(f"  {BOLD}{YELLOW}Enter your target domain to begin:{RESET}")
    print(f"  {DIM}Examples: lumen.com  /  example.com  /  target.io{RESET}\n")
    while True:
        target = input(f"  {GREEN}dorkboy{RESET}{DIM}@target>{RESET} {YELLOW}❯{RESET} ").strip()
        if target:
            break
        print(f"  {RED}Target cannot be empty. Please enter a domain.{RESET}")
    print(f"\n  {GREEN}✓ Target set: {BOLD}{target}{RESET}")
    time.sleep(0.5)

    while True:
        print_menu(target)
        choice = input(f"\n  {GREEN}dorkboy{RESET}{DIM}@{RESET}{GREEN}{target}{RESET} {YELLOW}❯{RESET} ").strip().upper()

        if choice == "Q":
            clear()
            print(f"\n{GREEN}{BANNER}{RESET}")
            print(f"  {CYAN}Thanks for using DORKBOY. Happy hunting!{RESET}")
            print(f"  {DIM}Remember: Only test on authorized targets.{RESET}\n")
            sys.exit(0)

        elif choice == "T":
            new_t = input(f"\n  {YELLOW}Enter new target domain:{RESET} ").strip()
            if new_t:
                target = new_t
                print(f"  {GREEN}✓ Target set to: {target}{RESET}")
                time.sleep(0.6)

        elif choice == "A":
            dump_all(target)

        elif choice == "S":
            search_dorks(target)

        elif choice in CATEGORIES:
            print_dork_list(choice, target)

        else:
            print(f"  {RED}Invalid choice. Try again.{RESET}")
            time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}Interrupted. Goodbye!{RESET}\n")
        sys.exit(0)
