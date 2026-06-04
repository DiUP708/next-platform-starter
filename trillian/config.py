"""Load .env and expose typed config. No runtime imports of dotenv needed — we read manually."""
import os, json, pathlib

ROOT = pathlib.Path(__file__).parent

def _load_env():
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, _, v = line.partition("=")
                k = k.strip()
                v = v.split("#")[0].strip()
                if k and k not in os.environ:
                    os.environ[k] = v

_load_env()

def get(key, default=""):
    return os.environ.get(key, default).strip()

GOOGLE_PLACES_API_KEY = get("GOOGLE_PLACES_API_KEY")
ANTHROPIC_API_KEY     = get("ANTHROPIC_API_KEY")
TELEGRAM_BOT_TOKEN    = get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID      = get("TELEGRAM_CHAT_ID")

SENDER_NAME      = get("SENDER_NAME", "Arvīds")
CALCOM_URL       = get("CALCOM_URL", "https://cal.com/arvids")
PORTFOLIO_URL    = get("PORTFOLIO_URL", "")
BASE_DEMO_URL    = get("BASE_DEMO_URL", "http://localhost:8000/demos")
SEND_MODE        = get("SEND_MODE", "draft")
DAILY_SEND_CAP   = int(get("DAILY_SEND_CAP", "30"))
BUDGET_USD       = float(get("BUDGET_USD_PER_DAY", "5"))
VPS_DEPLOY_TARGET= get("VPS_DEPLOY_TARGET", "")

CITIES  = ["Houston", "San Antonio", "Dallas", "Tampa", "Orlando", "Jacksonville", "Nashville", "Charlotte"]
NICHES  = ["roofing", "hvac"]
STATES  = {"Houston":"TX","San Antonio":"TX","Dallas":"TX","Tampa":"FL","Orlando":"FL",
           "Jacksonville":"FL","Nashville":"TN","Brentwood":"TN","Charlotte":"NC"}

NICHE_LABELS = {"roofing": "roofing", "hvac": "HVAC"}

# Colors per niche
NICHE_COLORS = {
    "roofing": {
        "primary_hex": "#1e2d40",   # deep navy
        "dark_hex":    "#111827",   # near-black
        "accent_hex":  "#e85d26",   # burnt orange
        "light":       "#fdf6f0",
    },
    "hvac": {
        "primary_hex": "#0f3460",   # deep navy-blue
        "dark_hex":    "#0a1929",   # very dark navy
        "accent_hex":  "#0ea5e9",   # sky blue
        "light":       "#f0f9ff",
    },
}

SERVICES = {
    "roofing": [
        {"icon": "🏠", "name": "Roof Repair",        "desc": "Fast, lasting fixes for leaks, missing shingles, and storm damage."},
        {"icon": "🔄", "name": "Full Replacement",   "desc": "New roof installed right — with a warranty that actually means something."},
        {"icon": "⛈️",  "name": "Storm Damage",      "desc": "Emergency response and insurance claim assistance after a storm."},
        {"icon": "🔍", "name": "Free Inspection",    "desc": "No-obligation 30-minute roof health check. Know before a problem grows."},
    ],
    "hvac": [
        {"icon": "❄️",  "name": "AC Repair",         "desc": "Same-day diagnosis and repair so you're not sweating it out."},
        {"icon": "🌡️", "name": "New Installation",  "desc": "Right-sized systems for your home — efficient and quiet."},
        {"icon": "🔥", "name": "Heating Service",   "desc": "Furnace tune-ups, repairs, and replacements before winter hits."},
        {"icon": "🔧", "name": "Maintenance Plans", "desc": "Preventive care that keeps your system running and your bills low."},
    ],
}
