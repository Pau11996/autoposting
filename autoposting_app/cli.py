import argparse
from datetime import datetime, timezone, timedelta
from typing import List

from .config import load_config
from .extract import extract_clean_text
from .fetch_feeds import fetch_feed_entries
from .post_telegram import format_for_telegram, send_telegram_message
from .store import filter_new_items, mark_posted
from .summarize import summarize_items


def collect_items(max_articles: int) -> List[dict]:
    cfg = load_config()
    entries = fetch_feed_entries(cfg.rss_sources(), max_per_feed=8)
    # Keep only items published yesterday in UTC (for daily digest)
    yesterday_utc = (datetime.now(tz=timezone.utc) - timedelta(days=1)).date()
    yesterdays_entries = [
        e
        for e in entries
        if e.get("published") and e["published"].astimezone(timezone.utc).date() == yesterday_utc
    ]
    fresh = filter_new_items(cfg.db_path, yesterdays_entries)
    top = fresh[:max_articles]
    enriched = []
    for it in top:
        content = extract_clean_text(it["link"]) or it.get("summary")
        enriched.append({**it, "content": content})
    return enriched


def run(post: bool, offline: bool, max_articles: int) -> int:
    cfg = load_config()
    items = collect_items(max_articles=max_articles)

    if not items:
        print("No new items found.")
        return 0

    # Determine language for summarization
    language = cfg.target_language if cfg.translate_posts else "english"
    
    summary_text = summarize_items(
        items,
        api_key=cfg.openai_api_key,
        model=cfg.llm_model,
        base_url=cfg.openai_base_url,
        offline=offline or cfg.offline_mode,
        language=language,
    )

    # Create a more engaging header with day of week
    now = datetime.now(tz=timezone.utc)
    
    if cfg.translate_posts and cfg.target_language.lower() == "russian":
        # Russian header format
        day_names = {
            "Monday": "Понедельник", "Tuesday": "Вторник", "Wednesday": "Среда",
            "Thursday": "Четверг", "Friday": "Пятница", "Saturday": "Суббота", "Sunday": "Воскресенье"
        }
        months = {
            "January": "января", "February": "февраля", "March": "марта", "April": "апреля",
            "May": "мая", "June": "июня", "July": "июля", "August": "августа",
            "September": "сентября", "October": "октября", "November": "ноября", "December": "декабря"
        }
        
        day_name = day_names.get(now.strftime("%A"), now.strftime("%A"))
        month_name = months.get(now.strftime("%B"), now.strftime("%B"))
        day_num = now.strftime("%d").lstrip("0")  # Remove leading zero
        year = now.strftime("%Y")
        
        header = f"Стартапы и Бизнес — {day_name}, {day_num} {month_name} {year}"
    else:
        # English header format
        day_name = now.strftime("%A")
        formatted_date = now.strftime("%B %d, %Y")
        header = f"Startups & Business — {day_name}, {formatted_date}"
    tg_text = format_for_telegram(summary_text, header=header, language=language)

    if post:
        if not (cfg.telegram_bot_token and cfg.telegram_chat_id):
            print("Missing TG_BOT_TOKEN or TG_CHAT_ID. Aborting post.")
            return 2
        ok = send_telegram_message(cfg.telegram_bot_token, cfg.telegram_chat_id, tg_text)
        if ok:
            for it in items:
                mark_posted(cfg.db_path, it["link"], it.get("title"))
            print("Posted to Telegram.")
            return 0
        else:
            print("Failed to post to Telegram.")
            return 1
    else:
        print(tg_text)
        return 0


def main():
    parser = argparse.ArgumentParser(description="Startup/Business news summarizer → Telegram")
    parser.add_argument("--post", action="store_true", help="Actually post to Telegram (otherwise dry-run)")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Offline mode: skip LLM and use titles only",
    )
    parser.add_argument("--max-articles", type=int, default=6, help="Max number of articles to include")
    parser.add_argument(
        "--language", 
        choices=["english", "russian"], 
        help="Output language (overrides config)"
    )
    parser.add_argument(
        "--no-translate",
        action="store_true",
        help="Disable translation (use English)"
    )
    args = parser.parse_args()

    # Override config with command line args if provided
    if args.language or args.no_translate:
        import os
        if args.no_translate:
            os.environ["TRANSLATE_POSTS"] = "false"
        elif args.language:
            os.environ["TARGET_LANGUAGE"] = args.language
            os.environ["TRANSLATE_POSTS"] = "true"

    code = run(post=args.post, offline=args.offline, max_articles=args.max_articles)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
