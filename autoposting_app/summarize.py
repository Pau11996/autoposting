from typing import List, Optional

from openai import OpenAI


SYSTEM_PROMPT = (
    "You are a professional finance and technology news analyst. Summarize startup and business news clearly and concisely for a Telegram audience."
)


def build_article_prompt(items: List[dict]) -> str:
    bullet_lines = []
    for idx, item in enumerate(items, start=1):
        line = f"{idx}. {item['title']} — {item.get('link', '')}"
        if item.get("content"):
            line += f"\nContent: {item['content'][:1500]}"
        bullet_lines.append(line)
    prompt = (
        "Create a concise summary of the following startup/business news items for a Telegram channel. "
        "Output should be 5-8 short bullets with strong headlines, each bullet 1-2 sentences, include the source link at the end in parentheses. "
        "Avoid hype; focus on facts, funding, launches, partnerships, and market moves. If multiple items are similar, merge them.\n\n"
        + "\n\n".join(bullet_lines)
    )
    return prompt


def summarize_items(
    items: List[dict],
    api_key: Optional[str],
    model: str,
    base_url: Optional[str] = None,
    offline: bool = False,
) -> str:
    if offline or not api_key:
        # Fallback summary without LLM
        bullets = []
        for item in items:
            bullets.append(f"- {item['title']} ({item.get('link','')})")
        return "\n".join(bullets)

    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

    user_prompt = build_article_prompt(items)

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=600,
    )
    text = completion.choices[0].message.content.strip()
    return text
