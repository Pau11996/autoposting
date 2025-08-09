# Focused startup and business news sources
# Curated for maximum relevance to entrepreneurs and business professionals

# Specialized source collections
STARTUP_FOCUSED_SOURCES = [
    "https://news.ycombinator.com/rss",                    # HackerNews - startup community
    "https://feeds.feedburner.com/TechCrunch/startups",   # TechCrunch startups
    "https://techcrunch.com/category/venture/feed/",      # TechCrunch venture capital
    "https://venturebeat.com/feed/",                      # VentureBeat - startup news
    "https://www.fastcompany.com/startup/rss",            # Fast Company startup
    "https://feeds.feedburner.com/crunchbase_daily",      # Crunchbase funding data
]

BUSINESS_NEWS_SOURCES = [
    "https://www.reuters.com/technology/rss",             # Reuters tech business
    "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",   # Wall Street Journal
    "https://www.ft.com/rss/companies/technology",       # Financial Times tech
    "https://www.fastcompany.com/technology/rss",        # Fast Company innovation
    "https://www.inc.com/rss/technology.rss",            # Inc Magazine business
]

# FOCUSED DEFAULT: Startup + Business news only (user's preference)
DEFAULT_RSS_SOURCES = STARTUP_FOCUSED_SOURCES + BUSINESS_NEWS_SOURCES

# Alternative comprehensive source set (previous default)
COMPREHENSIVE_SOURCES = [
    # === STARTUP & VENTURE CAPITAL ===
    "https://news.ycombinator.com/rss",
    "https://feeds.feedburner.com/TechCrunch/startups",
    "https://techcrunch.com/category/startups/feed/",
    "https://techcrunch.com/category/venture/feed/",
    "https://venturebeat.com/feed/",
    "https://feeds.feedburner.com/venturebeat/SZYF",
    
    # === BUSINESS & INNOVATION ===
    "https://www.fastcompany.com/technology/rss",
    "https://www.fastcompany.com/startup/rss",
    "https://www.theverge.com/rss/index.xml",
    "https://arstechnica.com/business/feed/",
    
    # === FINANCIAL & MARKET NEWS ===
    "https://www.reuters.com/technology/rss",
    "https://www.reuters.com/finance/markets/rss",
    "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "https://www.ft.com/rss/companies/technology",
    
    # === TECH INDUSTRY INSIGHTS ===
    "https://stratechery.com/feed/",
    "https://www.protocol.com/rss",
    "https://www.axios.com/newsletters/axios-login/rss",
    "https://www.wired.com/feed/category/business/latest/rss",
    
    # === ADDITIONAL QUALITY SOURCES ===
    "https://www.inc.com/rss/technology.rss",
    "https://www.forbes.com/entrepreneurs/feed2/",
    "https://feeds.feedburner.com/crunchbase_daily",
]

TECH_INDUSTRY_SOURCES = [
    "https://www.theverge.com/rss/index.xml",
    "https://arstechnica.com/business/feed/",
    "https://stratechery.com/feed/",
    "https://www.wired.com/feed/category/business/latest/rss",
]
