#!/usr/bin/env python3
"""
Trillian Studio — Main cycle runner.
Usage: python run.py [--once] [--step STEP]
Steps: find | build | deploy | emails | send | report
Default: run the full daily cycle.
"""
import argparse, csv, json, logging, pathlib, re, subprocess, sys, time
from datetime import date, datetime
import traceback

ROOT = pathlib.Path(__file__).parent

# ── logging setup ─────────────────────────────────────────────────────────────
log_file = ROOT / "logs" / f"{date.today()}.log"
log_file.parent.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, encoding="utf-8"),
    ],
)
log = logging.getLogger("run")


def _install(pkg: str):
    log.info(f"Installing {pkg}…")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "-q", pkg])


def _ensure_deps():
    missing = []
    try: import jinja2
    except ImportError: missing.append("jinja2")
    try: import requests
    except ImportError: missing.append("requests")
    for pkg in missing:
        _install(pkg)


_ensure_deps()

import config
import find_leads, build_demos, generate_emails
from notify import send as telegram


# ── state helpers ──────────────────────────────────────────────────────────────
STATE = ROOT / "state"
SPEND_FILE = STATE / "spend.json"


def _load_spend():
    if SPEND_FILE.exists():
        try:
            return json.loads(SPEND_FILE.read_text())
        except Exception:
            pass
    return {}


def _save_spend(d: dict):
    SPEND_FILE.write_text(json.dumps(d, indent=2))


def _today_spend() -> float:
    d = _load_spend()
    return float(d.get(str(date.today()), 0.0))


def _add_spend(amount: float):
    d = _load_spend()
    key = str(date.today())
    d[key] = round(float(d.get(key, 0.0)) + amount, 4)
    _save_spend(d)


# ── deploy step ────────────────────────────────────────────────────────────────
def step_deploy() -> list[str]:
    """Deploy demos/ to VPS and mark demo_live. Returns list of verified URLs."""
    import requests as req

    deploy_sh = ROOT / "deploy.sh"
    deploy_sh.chmod(0o755)
    try:
        result = subprocess.run(["bash", str(deploy_sh)], capture_output=True, text=True, timeout=120)
        log.info(result.stdout.strip())
        if result.returncode != 0:
            log.warning(f"deploy.sh stderr: {result.stderr}")
    except Exception as e:
        log.error(f"deploy.sh error: {e}")

    # Update master: demo_built → demo_live, verify HTTP 200
    master_path = STATE / "leads_master.csv"
    with open(master_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    fieldnames = [
        "place_id","name","niche","city","state","phone",
        "rating","reviews","website","score","status",
        "demo_url","first_seen","last_action",
    ]

    verified = []
    for row in rows:
        if row.get("status") != "demo_built":
            continue
        demo_url = row.get("demo_url", "")
        if not demo_url:
            continue

        # Verify the demo is reachable (skip if localhost in URL since server may not be running)
        ok = True
        if "localhost" not in demo_url:
            for attempt in range(3):
                try:
                    r = req.get(demo_url, timeout=10)
                    name_present = row["name"].split()[0].lower() in r.text.lower()
                    if r.status_code == 200 and name_present:
                        log.info(f"Verified {demo_url} ✓")
                        ok = True
                        break
                    else:
                        log.warning(f"Verify failed {demo_url}: status={r.status_code} name_present={name_present}")
                        ok = False
                except Exception as e:
                    log.warning(f"Verify attempt {attempt+1} error for {demo_url}: {e}")
                    time.sleep(2 ** attempt)
                    ok = False
        else:
            log.info(f"localhost demo — skipping HTTP check, marking live: {demo_url}")

        if ok:
            row["status"]      = "demo_live"
            row["last_action"] = str(date.today())
            verified.append(demo_url)

    with open(master_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    log.info(f"deploy: {len(verified)} demos marked live")
    return verified


# ── report builder ─────────────────────────────────────────────────────────────
def _build_report(new_leads, demos_built, drafts, sent_count, errors) -> str:
    master_path = STATE / "leads_master.csv"
    with open(master_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    hot   = sum(1 for r in rows if int(r.get("score",0)) == 3)
    warm  = sum(1 for r in rows if int(r.get("score",0)) == 2)
    total = len(rows)
    spend = _today_spend()

    lines = [
        f"<b>Trillian Studio — Daily Report {date.today()}</b>",
        f"",
        f"🔍 <b>Leads</b>: {len(new_leads)} new (HOT: {hot} total, WARM: {warm} total, total in DB: {total})",
        f"🏗️ <b>Demos built</b>: {len(demos_built)}",
        f"✉️ <b>Emails drafted</b>: {len(drafts)} | Sent: {sent_count}",
        f"💸 <b>Spend today</b>: ${spend:.2f} / ${config.BUDGET_USD:.2f}",
        f"📋 <b>SEND_MODE</b>: {config.SEND_MODE}",
    ]
    if errors:
        lines.append(f"")
        lines.append(f"⚠️ <b>Errors ({len(errors)})</b>:")
        for e in errors[:5]:
            lines.append(f"  · {e}")
    lines += [
        f"",
        f"Preview demos: <code>cd /opt/trillian && python -m http.server 8000</code>",
        f"then open http://localhost:8000/demos/",
    ]
    return "\n".join(lines)


# ── main cycle ─────────────────────────────────────────────────────────────────
def run_cycle(steps=None):
    all_steps = ["find", "build", "deploy", "emails", "send", "report"]
    steps = steps or all_steps
    errors = []
    new_leads, demos_built, drafts, sent_count = [], [], [], 0

    log.info(f"=== Trillian cycle start {datetime.now().isoformat()} ===")
    log.info(f"SEND_MODE={config.SEND_MODE}  steps={steps}")

    # ── 1. Find leads ──────────────────────────────────────────────────────────
    if "find" in steps:
        try:
            new_leads = find_leads.run()
            log.info(f"find: {len(new_leads)} new")
        except Exception as e:
            tb = traceback.format_exc()
            log.error(f"find_leads failed: {e}")
            (ROOT/"errors"/f"find_{date.today()}.txt").write_text(tb)
            errors.append(f"find_leads: {e}")

    # ── 2. Build demos ─────────────────────────────────────────────────────────
    if "build" in steps:
        try:
            demos_built = build_demos.run()
            log.info(f"build: {len(demos_built)} demos")
        except Exception as e:
            tb = traceback.format_exc()
            log.error(f"build_demos failed: {e}")
            (ROOT/"errors"/f"build_{date.today()}.txt").write_text(tb)
            errors.append(f"build_demos: {e}")

    # ── 3. Deploy + verify ─────────────────────────────────────────────────────
    if "deploy" in steps:
        try:
            verified = step_deploy()
            log.info(f"deploy: {len(verified)} live")
        except Exception as e:
            tb = traceback.format_exc()
            log.error(f"deploy failed: {e}")
            (ROOT/"errors"/f"deploy_{date.today()}.txt").write_text(tb)
            errors.append(f"deploy: {e}")

    # ── 4. Draft emails ────────────────────────────────────────────────────────
    if "emails" in steps:
        try:
            drafts = generate_emails.run()
            log.info(f"emails: {len(drafts)} drafted")
        except Exception as e:
            tb = traceback.format_exc()
            log.error(f"generate_emails failed: {e}")
            (ROOT/"errors"/f"emails_{date.today()}.txt").write_text(tb)
            errors.append(f"generate_emails: {e}")

    # ── 5. Send (respects SEND_MODE) ───────────────────────────────────────────
    if "send" in steps:
        if config.SEND_MODE == "draft":
            log.info("SEND_MODE=draft — not sending, emails saved to emails/")
        elif config.SEND_MODE == "approve":
            # Collect drafts, ping user
            email_dir = ROOT / "emails"
            pending = list(email_dir.glob("*.md"))
            if pending:
                msg = f"📬 <b>{len(pending)} emails ready for approval</b>\n"
                msg += "\n".join(f"  · {p.stem}" for p in pending[:10])
                msg += f"\n\nReply GO to send, or SKIP to queue for tomorrow."
                telegram(msg)
                log.info(f"Queued {len(pending)} emails for approval — Telegram ping sent")
        elif config.SEND_MODE == "api":
            log.info("SEND_MODE=api — cold-email provider integration not yet wired up")
            errors.append("SEND_MODE=api: provider integration needed (Instantly/Smartlead)")

    # ── 6. Report ──────────────────────────────────────────────────────────────
    if "report" in steps:
        report = _build_report(new_leads, demos_built, drafts, sent_count, errors)
        log.info(f"\n{'='*60}\nDAILY REPORT\n{'='*60}\n{report}\n{'='*60}")
        telegram(report)

    log.info(f"=== Trillian cycle done {datetime.now().isoformat()} ===")
    return {"new_leads": len(new_leads), "demos": len(demos_built), "drafts": len(drafts), "errors": errors}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--step", nargs="*", help="Run specific steps only")
    args = parser.parse_args()
    run_cycle(steps=args.step)
