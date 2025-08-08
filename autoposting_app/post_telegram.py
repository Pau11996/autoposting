import html
from typing import Optional

import requests


def send_telegram_message(
    bot_token: str,
    chat_id: str,
    text: str,
    disable_web_page_preview: bool = True,
    parse_mode: str = "HTML",
) -> bool:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": disable_web_page_preview,
        "parse_mode": parse_mode,
    }
    try:
        resp = requests.post(url, json=payload, timeout=20)
        return resp.ok
    except Exception:
        return False


def format_for_telegram(summary_text: str, header: Optional[str] = None) -> str:
    max_len = 4096
    if header:
        header_html = f"<b>{html.escape(header)}</b>\n\n"
    else:
        header_html = ""
    text = header_html + html.escape(summary_text)
    if len(text) > max_len:
        text = text[: max_len - 50] + "..."
    return text
