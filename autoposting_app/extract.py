from typing import Optional

import trafilatura


def extract_clean_text(url: str, timeout: int = 20) -> Optional[str]:
    try:
        downloaded = trafilatura.fetch_url(url, timeout=timeout)
        if not downloaded:
            return None
        text = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
        if text:
            return text.strip()
        return None
    except Exception:
        return None
