## Autoposting: Startup/Business News Summarizer → Telegram

Summarizes startup/business news from RSS feeds using an LLM and posts a concise digest to your Telegram channel.

### Features
- Fetches from popular startup/business RSS feeds (override via env)
- Extracts article text for better summarization
- Summarizes with OpenAI Chat Completions (model configurable)
- Posts to Telegram; keeps a small SQLite DB to avoid duplicates

---

## Requirements
- Python 3.10+ (for local runs)
- Docker (optional, for container runs)
- Telegram Bot token (from BotFather) and your channel ID
- OpenAI API key (if not running in `--offline` mode)

---

## Environment variables
- `OPENAI_API_KEY` (required for non-offline runs)
- `LLM_MODEL` (default: `gpt-4o-mini`; set to a model you have access to, e.g. `gpt-4o`, `gpt-4.1`, or `gpt-5`)
- `OPENAI_BASE_URL` (optional custom endpoint)
- `TG_BOT_TOKEN` (Telegram bot token)
- `TG_CHAT_ID` (channel ID like `-1001234567890` or `@channelusername`)
- `RSS_SOURCES` (comma-separated RSS URLs to override defaults)
- `MAX_ARTICLES` (default: `6`)
- `DB_PATH` (default: `data/autoposting.db`)

To get your channel ID, add your bot as an admin to the channel, post a message, then run:
```bash
curl "https://api.telegram.org/bot$TG_BOT_TOKEN/getUpdates"
```
Look for `chat.id` (e.g. `-100...`).

---

## Run with Docker (recommended)
Build the image:
```bash
docker build -t autoposting .
```

Dry-run (no Telegram post, uses titles if no API key):
```bash
docker run --rm \
  -e MAX_ARTICLES=2 \
  -e OFFLINE_MODE=true \
  -v "$(pwd)/data:/app/data" \
  autoposting --offline --max-articles 2
```

Post to Telegram (live):
```bash
 docker run --rm   --env-file .env   -v "$(pwd)/data:/app/data"   autoposting --post --max-articles 
```

Override RSS sources:
```bash
docker run --rm \
  -e OPENAI_API_KEY="sk-..." \
  -e TG_BOT_TOKEN="123456:ABC..." \
  -e TG_CHAT_ID="-1001234567890" \
  -e RSS_SOURCES="https://news.ycombinator.com/rss,https://feeds.feedburner.com/TechCrunch/startups" \
  -v "$(pwd)/data:/app/data" \
  autoposting --post
```

Note: Mounting `$(pwd)/data:/app/data` keeps the SQLite DB persistent across runs, avoiding duplicate posts.

---

## Run locally (alternative)
Create a virtualenv, install dependencies, and run:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Dry-run (no Telegram post)
python main.py --offline --max-articles 6

# Live post
export OPENAI_API_KEY="sk-..."
export TG_BOT_TOKEN="123456:ABC..."
export TG_CHAT_ID="-1001234567890"
python main.py --post --max-articles 6
```

---

## Customize feeds
- Set `RSS_SOURCES` to a comma-separated list of RSS URLs, or edit the defaults in `autoposting_app/news_sources.py`.

## Scheduling
- Use cron (local) or a container scheduler to run periodically, e.g. hourly. Example cron (local):
```bash
0 * * * * cd /path/to/autoposting && /usr/bin/bash -lc 'source .venv/bin/activate && OPENAI_API_KEY=sk-... TG_BOT_TOKEN=... TG_CHAT_ID=... python main.py --post --max-articles 6' >> cron.log 2>&1
```

---

### Commands help
```bash
python main.py -h
# or with Docker
docker run --rm autoposting -h
```
