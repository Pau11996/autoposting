import argparse
from datetime import datetime, timezone
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
    fresh = filter_new_items(cfg.db_path, entries)
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

    summary_text = summarize_items(
        items,
        api_key=cfg.openai_api_key,
        model=cfg.llm_model,
        base_url=cfg.openai_base_url,
        offline=offline or cfg.offline_mode,
    )

    header = datetime.now(tz=timezone.utc).strftime("Startups & Business — %Y-%m-%d")
    tg_text = format_for_telegram(summary_text, header=header)

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
    args = parser.parse_args()

    code = run(post=args.post, offline=args.offline, max_articles=args.max_articles)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
