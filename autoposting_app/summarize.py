from typing import List, Optional

from openai import OpenAI


SYSTEM_PROMPT_ENGLISH = (
    "You are a professional finance and technology news analyst creating engaging content for a Telegram audience. "
    "Write in a conversational, accessible tone that makes complex business news easy to understand. "
    "Use engaging headlines and focus on the human impact and practical implications of news stories."
)

SYSTEM_PROMPT_RUSSIAN = (
    "Вы профессиональный аналитик финансовых и технологических новостей, создающий увлекательный контент для аудитории Telegram. "
    "Пишите в разговорном, доступном тоне, который делает сложные бизнес-новости легкими для понимания. "
    "Используйте привлекательные заголовки и сосредоточьтесь на человеческом воздействии и практических последствиях новостей."
)


def build_article_prompt(items: List[dict], language: str = "english") -> str:
    bullet_lines = []
    for idx, item in enumerate(items, start=1):
        line = f"{idx}. {item['title']} — {item.get('link', '')}"
        if item.get("content"):
            line += f"\nContent: {item['content'][:1500]}"
        bullet_lines.append(line)
    
    if language.lower() == "russian":
        prompt = (
            "Создайте увлекательную сводку следующих новостей стартапов/бизнеса для аудитории Telegram. "
            "Формат: 4-6 новостных элементов, каждый с:\n"
            "• Привлекательным заголовком с соответствующими эмодзи\n"
            "• 2-3 предложениями, объясняющими ключевые факты и почему это важно\n"
            "• Стратегическое использование эмодзи для улучшения читаемости\n"
            "• Группировка похожих историй вместе\n"
            "• Фокус на раундах финансирования, запусках продуктов, партнерствах, рыночных трендах и кадровых изменениях\n"
            "• Сделайте контент удобным для сканирования и привлекательным для занятых профессионалов\n"
            "• Укажите домен источника (не полный URL) в квадратных скобках после каждого элемента\n"
            "• ВАЖНО: Отвечайте ТОЛЬКО на русском языке\n\n"
            + "\n\n".join(bullet_lines)
        )
    else:
        prompt = (
            "Create an engaging summary of the following startup/business news for a Telegram audience. "
            "Format as 4-6 news items, each with:\n"
            "• A compelling headline with relevant emoji\n"
            "• 2-3 sentences explaining the key facts and why it matters\n"
            "• Use emojis strategically to enhance readability\n"
            "• Group similar stories together\n"
            "• Focus on funding rounds, product launches, partnerships, market trends, and leadership changes\n"
            "• Make it scannable and engaging for busy professionals\n"
            "• Include the source domain (not full URL) in brackets after each item\n\n"
            + "\n\n".join(bullet_lines)
        )
    return prompt


def summarize_items(
    items: List[dict],
    api_key: Optional[str],
    model: str,
    base_url: Optional[str] = None,
    offline: bool = False,
    language: str = "english",
) -> str:
    if offline or not api_key:
        # Fallback summary without LLM - make it more user-friendly
        bullets = []
        for idx, item in enumerate(items, 1):
            # Add simple emoji based on content keywords
            title_lower = item['title'].lower()
            emoji = "📈" if any(word in title_lower for word in ['funding', 'raised', 'investment', 'финансирование', 'инвестиции']) else \
                   "🚀" if any(word in title_lower for word in ['launch', 'release', 'debut', 'запуск', 'релиз']) else \
                   "🤝" if any(word in title_lower for word in ['partnership', 'deal', 'acquisition', 'партнерство', 'сделка']) else \
                   "💼"
            
            # Extract domain from URL for cleaner display
            link = item.get('link', '')
            try:
                from urllib.parse import urlparse
                domain = urlparse(link).netloc.replace('www.', '')
            except:
                domain = link
            
            if language.lower() == "russian":
                # Simple translation for common business terms in headlines
                title = item['title']
                # Note: This is basic keyword replacement. For full translation, API is needed.
                bullets.append(f"{emoji} <b>{title}</b>\n   [{domain}]")
            else:
                bullets.append(f"{emoji} <b>{item['title']}</b>\n   [{domain}]")
        
        return "\n\n".join(bullets)

    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

    user_prompt = build_article_prompt(items, language)
    
    # Select appropriate system prompt based on language
    system_prompt = SYSTEM_PROMPT_RUSSIAN if language.lower() == "russian" else SYSTEM_PROMPT_ENGLISH

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,  # Slightly more creative for engaging content
        max_tokens=800,   # More space for detailed, well-formatted content
    )
    text = completion.choices[0].message.content.strip()
    return text
