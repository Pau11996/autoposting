import os
from dataclasses import dataclass, field
from typing import List, Optional

from dotenv import load_dotenv


load_dotenv()


@dataclass
class AppConfig:
    # LLM
    openai_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY")
    )
    openai_base_url: Optional[str] = field(
        default_factory=lambda: os.getenv("OPENAI_BASE_URL")
    )
    llm_model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-4o-mini"))

    # Telegram
    telegram_bot_token: Optional[str] = field(
        default_factory=lambda: os.getenv("TG_BOT_TOKEN")
    )
    telegram_chat_id: Optional[str] = field(
        default_factory=lambda: os.getenv("TG_CHAT_ID")
    )

    # App behavior
    max_articles: int = field(default_factory=lambda: int(os.getenv("MAX_ARTICLES", "6")))
    offline_mode: bool = field(
        default_factory=lambda: os.getenv("OFFLINE_MODE", "false").lower() in {"1", "true", "yes"}
    )
    db_path: str = field(default_factory=lambda: os.getenv("DB_PATH", "data/autoposting.db"))

    # Sources (CSV in env or default list)
    rss_sources_csv: Optional[str] = field(
        default_factory=lambda: os.getenv("RSS_SOURCES")
    )

    def rss_sources(self) -> List[str]:
        if self.rss_sources_csv:
            return [s.strip() for s in self.rss_sources_csv.split(",") if s.strip()]
        from .news_sources import DEFAULT_RSS_SOURCES

        return DEFAULT_RSS_SOURCES


def load_config() -> AppConfig:
    return AppConfig()
