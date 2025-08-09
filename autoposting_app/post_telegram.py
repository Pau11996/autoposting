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


def format_for_telegram(summary_text: str, header: Optional[str] = None, language: str = "english") -> str:
    max_len = 4096
    
    # Create an engaging header with emojis
    if header:
        # Extract date from header and make it more visual
        if "—" in header:
            title_part, date_part = header.split("—", 1)
            header_html = f"📰 <b>{html.escape(title_part.strip())}</b>\n🗓 {html.escape(date_part.strip())}\n\n"
        else:
            header_html = f"📰 <b>{html.escape(header)}</b>\n\n"
    else:
        header_html = ""
    
    # Add separator line for better visual structure
    separator = "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    # Don't escape HTML if it's already formatted (from LLM or offline mode)
    if any(tag in summary_text for tag in ['<b>', '<i>', '<code>', '<pre>', '<a>']):
        # Already has HTML formatting
        formatted_summary = summary_text
    else:
        # Plain text, needs escaping
        formatted_summary = html.escape(summary_text)
    
    # Add footer with subtle branding (language-specific)
    if language.lower() == "russian":
        footer = f"\n\n━━━━━━━━━━━━━━━━━━━━\n💡 <i>Работает на ИИ • Обновляется ежедневно</i>"
        truncated_text = "... <i>(сокращено)</i>"
    else:
        footer = f"\n\n━━━━━━━━━━━━━━━━━━━━\n💡 <i>Powered by AI • Updated daily</i>"
        truncated_text = "... <i>(truncated)</i>"
    
    text = header_html + separator + formatted_summary + footer
    
    # Smart truncation that preserves structure
    if len(text) > max_len:
        # Try to truncate at a logical break point
        truncate_at = max_len - 100
        last_line_break = text.rfind('\n', 0, truncate_at)
        if last_line_break > truncate_at - 200:  # If we found a reasonable break point
            text = text[:last_line_break] + f"\n\n{truncated_text}" + footer
        else:
            text = text[:max_len - 50] + "..."
    
    return text
