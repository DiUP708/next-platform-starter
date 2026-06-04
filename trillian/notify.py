"""Send Telegram message. No-op if bot token / chat_id not set."""
import requests, logging
import config

log = logging.getLogger(__name__)


def send(text: str):
    token = config.TELEGRAM_BOT_TOKEN
    chat  = config.TELEGRAM_CHAT_ID
    if not token or not chat:
        log.info(f"[Telegram not configured] {text[:80]}")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": chat, "text": text, "parse_mode": "HTML"}, timeout=10)
        r.raise_for_status()
    except Exception as e:
        log.warning(f"Telegram send failed: {e}")
