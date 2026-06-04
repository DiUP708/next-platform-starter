"""
Draft personalized emails for demo_live leads.
Saves to emails/{slug}.md. Never sends — that's run.py's job.
Also drafts follow-ups (day 3, day 7) for non-responders.
"""
import csv, re, pathlib, logging
from datetime import date, timedelta
import config

log = logging.getLogger(__name__)
ROOT       = pathlib.Path(__file__).parent
STATE      = ROOT / "state" / "leads_master.csv"
EMAILS_DIR = ROOT / "emails"
FIELDNAMES = [
    "place_id","name","niche","city","state","phone",
    "rating","reviews","website","score","status",
    "demo_url","first_seen","last_action",
]

VARIANT_A = """\
Subject: built a new website for {name}

Hi there,

I came across {name} — {rating}★ on Google, and clearly your customers love the work.

I build websites for {niche_label} companies that turn that reputation into more quote calls, \
and I went ahead and built a quick demo of what a new site for {name} could look like:

{demo_url}

No cost and no obligation — if it's not for you, no problem. If you like it, \
I can have the real version live in 7 days, and you don't pay unless you love it.

Want to grab 10 minutes this week? {calcom_url}

— {sender_name} | Trillian Studio
"""

FOLLOW_UP_3 = """\
Subject: Re: built a new website for {name}

Hi,

Just circling back — I know things get busy. Here's that demo link again:

{demo_url}

Takes 30 seconds to look at. If it's not a fit, just say the word and I'll leave you alone.

— {sender_name}
"""

FOLLOW_UP_7 = """\
Subject: Last note — {name} demo

Hi,

One last note from me — I'll leave you alone after this.

I built a free demo site for {name} ({demo_url}) and I'd hate for it to go to waste. \
If there's any interest, even just a quick look, I'm easy to reach:

{calcom_url}

Either way, wish you and the team a great week.

— {sender_name} | Trillian Studio
"""


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _load_master():
    with open(STATE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _save_master(rows):
    with open(STATE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def _draft(slug: str, content: str):
    EMAILS_DIR.mkdir(exist_ok=True)
    (EMAILS_DIR / f"{slug}.md").write_text(content, encoding="utf-8")


def run() -> list[dict]:
    rows  = _load_master()
    today = date.today()
    drafted = []

    for row in rows:
        status = row.get("status", "")
        slug   = _slug(row["name"])

        # Variant A — first outreach
        if status == "demo_live":
            niche_label = config.NICHE_LABELS.get(row.get("niche","roofing"), "roofing")
            body = VARIANT_A.format(
                name        = row["name"],
                rating      = row.get("rating", "5.0"),
                niche_label = niche_label,
                demo_url    = row.get("demo_url", ""),
                calcom_url  = config.CALCOM_URL,
                sender_name = config.SENDER_NAME,
            )
            _draft(slug, body)
            row["status"]      = "email_drafted"
            row["last_action"] = str(today)
            drafted.append(row)
            log.info(f"Drafted email for {row['name']}")
            continue

        # Follow-ups for non-responders
        if status == "sent":
            last = row.get("last_action", "")
            try:
                last_date = date.fromisoformat(last)
            except Exception:
                continue
            days_since = (today - last_date).days
            fu_slug = None
            body    = None
            if days_since >= 7:
                fu_slug = f"{slug}-followup2"
                body    = FOLLOW_UP_7.format(
                    name        = row["name"],
                    demo_url    = row.get("demo_url",""),
                    calcom_url  = config.CALCOM_URL,
                    sender_name = config.SENDER_NAME,
                )
            elif days_since >= 3:
                fu_slug = f"{slug}-followup1"
                body    = FOLLOW_UP_3.format(
                    name        = row["name"],
                    demo_url    = row.get("demo_url",""),
                    sender_name = config.SENDER_NAME,
                )
            if fu_slug and body:
                _draft(fu_slug, body)
                log.info(f"Drafted follow-up for {row['name']} (day {days_since})")

    _save_master(rows)
    log.info(f"generate_emails: {len(drafted)} initial drafts")
    return drafted
