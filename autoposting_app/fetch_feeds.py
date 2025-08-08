from datetime import datetime, timezone
from typing import Dict, List

import feedparser


def parse_datetime(entry) -> datetime:
    # Try to get published_parsed; fallback to now
    try:
        if hasattr(entry, "published_parsed") and entry.published_parsed is not None:
            return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        if hasattr(entry, "updated_parsed") and entry.updated_parsed is not None:
            return datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
    except Exception:
        pass
    return datetime.now(tz=timezone.utc)


def fetch_feed_entries(rss_urls: List[str], max_per_feed: int = 10) -> List[Dict]:
    entries: List[Dict] = []
    for url in rss_urls:
        try:
            parsed = feedparser.parse(url)
            for entry in parsed.entries[:max_per_feed]:
                link = getattr(entry, "link", None)
                title = getattr(entry, "title", None)
                summary = getattr(entry, "summary", "")
                published_dt = parse_datetime(entry)
                if link and title:
                    entries.append(
                        {
                            "link": link,
                            "title": title,
                            "summary": summary,
                            "published": published_dt,
                            "source": url,
                        }
                    )
        except Exception:
            continue
    # Sort newest first
    entries.sort(key=lambda e: e["published"], reverse=True)
    return entries
