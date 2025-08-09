import os
import time
from datetime import datetime, timedelta, timezone

from .cli import run
from .config import load_config


def seconds_until_target_utc(hour: int = 6, minute: int = 46) -> int:
    now = datetime.now(tz=timezone.utc)
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return int((target - now).total_seconds())


def main() -> None:
    cfg = load_config()
    post_flag_env = os.getenv("POST_TO_TG", "true").lower() in {"1", "true", "yes", "y"}
    
    # Log configuration at startup
    language_status = f"Russian translation: {'ON' if cfg.translate_posts else 'OFF'}"
    if cfg.translate_posts:
        language_status += f" (target: {cfg.target_language})"
    print(f"[scheduler] Starting with {language_status}")
    
    while True:
        sleep_seconds = seconds_until_target_utc(cfg.posting_hour, cfg.posting_minute)
        print(f"[scheduler] Sleeping {sleep_seconds}s until {cfg.posting_hour:02d}:{cfg.posting_minute:02d} UTC...")
        time.sleep(max(1, sleep_seconds))
        try:
            started = datetime.now(tz=timezone.utc).isoformat()
            print(f"[scheduler] Running job at {started}")
            code = run(post=post_flag_env, offline=cfg.offline_mode, max_articles=cfg.max_articles)
            finished = datetime.now(tz=timezone.utc).isoformat()
            print(f"[scheduler] Job finished with code={code} at {finished}")
        except Exception as exc:  # noqa: BLE001 - broad to keep loop alive
            import traceback

            print(f"[scheduler] Error during scheduled run: {exc}")
            traceback.print_exc()
        # Small guard to avoid immediate retrigger due to clock drift
        time.sleep(2)


if __name__ == "__main__":
    main()


