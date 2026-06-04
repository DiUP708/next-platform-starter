"""
Find and qualify leads.
- If GOOGLE_PLACES_API_KEY is set: query Google Places (New) API.
- Otherwise: load from leads_seed.csv (all get score=2, WARM).
Dedupes against leads_master.csv by place_id / name+city.
"""
import csv, json, time, logging, pathlib, re, requests
from datetime import date
import config

log = logging.getLogger(__name__)
ROOT = pathlib.Path(__file__).parent
STATE_FILE = ROOT / "state" / "leads_master.csv"

FIELDNAMES = [
    "place_id","name","niche","city","state","phone",
    "rating","reviews","website","score","status",
    "demo_url","first_seen","last_action",
]


def _load_master():
    if not STATE_FILE.exists() or STATE_FILE.stat().st_size < 5:
        return []
    with open(STATE_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _save_master(rows):
    with open(STATE_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _score(row: dict) -> int:
    reviews = int(row.get("review_count") or row.get("reviews") or 0)
    rating  = float(row.get("rating") or 0)
    website = (row.get("website") or row.get("websiteUri") or "").strip()
    if rating < 3.5:
        return 0
    if reviews > 500:
        return 0
    if not website:
        return 3   # HOT — no website
    if reviews < 150:
        return 2   # WARM — weak site
    return 1       # low priority but keep


def _from_seed() -> list[dict]:
    seed = ROOT / "leads_seed.csv"
    rows = []
    with open(seed, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({
                "place_id":    f"seed-{_slug(r['name'])}-{r['city'].lower()}",
                "name":        r["name"],
                "niche":       r["niche"],
                "city":        r["city"],
                "state":       r["state"],
                "phone":       r.get("phone", ""),
                "rating":      float(r.get("rating", 4.5)),
                "reviews":     int(r.get("review_count", 0)),
                "website":     "",
                "score":       _score(r),
                "status":      "discovered",
                "demo_url":    "",
                "first_seen":  str(date.today()),
                "last_action": str(date.today()),
            })
    return rows


def _from_places() -> list[dict]:
    """Query Google Places (New) for each city/niche combo."""
    api_key = config.GOOGLE_PLACES_API_KEY
    results = []
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.id,places.displayName,places.nationalPhoneNumber,places.rating,places.userRatingCount,places.websiteUri,places.addressComponents",
    }
    for city in config.CITIES:
        for niche in config.NICHES:
            query = f"{niche} companies in {city}"
            body  = {"textQuery": query, "maxResultCount": 20}
            for attempt in range(3):
                try:
                    resp = requests.post(url, headers=headers, json=body, timeout=15)
                    resp.raise_for_status()
                    break
                except Exception as e:
                    log.warning(f"Places API attempt {attempt+1} failed for {query}: {e}")
                    time.sleep(2 ** attempt)
            else:
                log.error(f"Places API failed 3x for {query}")
                continue

            for p in resp.json().get("places", []):
                state_code = ""
                for comp in p.get("addressComponents", []):
                    if "administrative_area_level_1" in comp.get("types", []):
                        state_code = comp.get("shortText", "")
                row = {
                    "place_id":    p["id"],
                    "name":        p.get("displayName", {}).get("text", ""),
                    "niche":       niche,
                    "city":        city,
                    "state":       state_code,
                    "phone":       p.get("nationalPhoneNumber", ""),
                    "rating":      float(p.get("rating", 0)),
                    "reviews":     int(p.get("userRatingCount", 0)),
                    "website":     p.get("websiteUri", ""),
                    "score":       0,
                    "status":      "discovered",
                    "demo_url":    "",
                    "first_seen":  str(date.today()),
                    "last_action": str(date.today()),
                }
                row["score"] = _score(row)
                results.append(row)
    return results


def run() -> list[dict]:
    """Return newly-added leads (appended to master)."""
    master = _load_master()
    known_ids = {r["place_id"] for r in master}

    if config.GOOGLE_PLACES_API_KEY:
        log.info("Using Google Places API")
        candidates = _from_places()
    else:
        log.info("No GOOGLE_PLACES_API_KEY — loading leads_seed.csv")
        candidates = _from_seed()

    added = []
    for r in candidates:
        if r["place_id"] in known_ids:
            continue
        if r["score"] == 0:
            continue
        master.append(r)
        known_ids.add(r["place_id"])
        added.append(r)

    # Sort: HOT first, then by rating desc
    master.sort(key=lambda x: (-int(x.get("score",0)), -float(x.get("rating",0))))
    _save_master(master)
    log.info(f"find_leads: {len(added)} new leads added (total {len(master)})")
    return added
