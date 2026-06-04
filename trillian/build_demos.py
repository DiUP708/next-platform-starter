"""
Build a self-contained HTML demo for each HOT/WARM lead.
Renders templates/demo.html.j2 → demos/{slug}/index.html
Then regenerates demos/index.html (internal gallery).
"""
import csv, re, pathlib, logging
from jinja2 import Environment, FileSystemLoader
from datetime import date
import config

log = logging.getLogger(__name__)
ROOT      = pathlib.Path(__file__).parent
STATE     = ROOT / "state" / "leads_master.csv"
DEMOS_DIR = ROOT / "demos"
TMPL_DIR  = ROOT / "templates"
FIELDNAMES = [
    "place_id","name","niche","city","state","phone",
    "rating","reviews","website","score","status",
    "demo_url","first_seen","last_action",
]


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


def _tagline(niche: str, name: str, city: str) -> str:
    if niche == "roofing":
        return f"{{ city }}'s Most Trusted Roofers — Done Right, on Time".replace("{{ city }}", city)
    return f"Fast, Reliable HVAC Service in {{ city }}".replace("{{ city }}", city)


def build_demo(lead: dict, env: Environment) -> pathlib.Path:
    niche  = lead.get("niche", "roofing")
    colors = config.NICHE_COLORS.get(niche, config.NICHE_COLORS["roofing"])
    slug   = _slug(lead["name"])
    out    = DEMOS_DIR / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)

    tmpl_name = f"demo_{niche}.html.j2"
    # fall back to generic demo template
    tmpl_file = TMPL_DIR / tmpl_name
    if not tmpl_file.exists():
        tmpl_name = "demo.html.j2"

    tmpl = env.get_template(tmpl_name)
    html = tmpl.render(
        name     = lead["name"],
        city     = lead["city"],
        state    = lead.get("state", ""),
        phone    = lead.get("phone", ""),
        rating   = lead.get("rating", "5.0"),
        reviews  = lead.get("reviews", "50"),
        niche    = niche,
        tagline  = _tagline(niche, lead["name"], lead["city"]),
        services = config.SERVICES[niche],
        **colors,
    )
    out.write_text(html, encoding="utf-8")
    log.info(f"Built demo: {out}")
    return out


def _build_gallery(rows: list[dict]):
    """demos/index.html — internal overview page."""
    cards = []
    for r in rows:
        if not r.get("demo_url"):
            continue
        slug   = _slug(r["name"])
        colors = config.NICHE_COLORS.get(r.get("niche","roofing"), config.NICHE_COLORS["roofing"])
        accent = colors["accent_hex"]
        cards.append(
            f'<div class="bg-white rounded-xl shadow p-5 border-t-4" style="border-color:{accent}">'
            f'<span class="text-xs font-bold uppercase px-2 py-1 rounded" style="background:{accent};color:#fff">{r.get("niche","")}</span>'
            f'<h3 class="font-bold text-lg mt-3">{r["name"]}</h3>'
            f'<p class="text-sm text-gray-500">{r.get("city","")}, {r.get("state","")}</p>'
            f'<p class="text-sm text-gray-500">{r.get("rating","")}★ · {r.get("reviews","")} reviews · score {r.get("score","")}</p>'
            f'<p class="text-sm mt-1 text-gray-600">Status: <strong>{r.get("status","")}</strong></p>'
            f'<a href="{slug}/" class="mt-3 inline-block text-sm font-bold underline" style="color:{accent}">View Demo →</a>'
            f'</div>'
        )
    gallery_html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Trillian Studio — Demo Gallery</title>
<script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-gray-100 min-h-screen p-8">
<div class="max-w-6xl mx-auto">
<h1 class="text-3xl font-extrabold text-gray-800 mb-2">Trillian Studio · Demo Gallery</h1>
<p class="text-gray-500 mb-8">Generated {date.today()} · {len(cards)} demos</p>
<div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">{"".join(cards)}</div>
</div></body></html>"""
    (DEMOS_DIR / "index.html").write_text(gallery_html, encoding="utf-8")


def run() -> list[dict]:
    """Build demos for leads that need one. Return updated rows."""
    rows = _load_master()
    env  = Environment(loader=FileSystemLoader(str(TMPL_DIR)))
    built = []

    for row in rows:
        score  = int(row.get("score", 0))
        status = row.get("status", "")
        if score < 1 or status not in ("discovered",):
            continue
        try:
            slug   = _slug(row["name"])
            out    = build_demo(row, env)
            demo_path = f"{config.BASE_DEMO_URL}/{slug}/"
            row["demo_url"]    = demo_path
            row["status"]      = "demo_built"
            row["last_action"] = str(date.today())
            built.append(row)
        except Exception as e:
            log.error(f"build_demos failed for {row['name']}: {e}", exc_info=True)

    _save_master(rows)
    _build_gallery(rows)
    log.info(f"build_demos: {len(built)} demos built")
    return built
