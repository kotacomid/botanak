# 📚 Book Scraping Bot - Comprehensive Auto Scraper

A powerful, modular bot for scraping book metadata from Anna's Archive & LibGen with automatic download, upload, and content generation capabilities.

## 🚀 Features

### Core Features (Free Tier)
- ✅ Metadata scraping from Anna's Archive & LibGen
- ✅ Book file and cover image download
- ✅ Google Drive & FTP upload
- ✅ JSON/CSV/HTML output generation
- ✅ WordPress/Blogspot auto-posting
- ✅ Basic affiliate link integration

### Advanced Features (Paid Tier)
- 🔥 AI-powered video generation for social media
- 🔥 Advanced metadata enrichment
- 🔥 Telegram bot notifications
- 🔥 Multi-platform posting automation
- 🔥 Advanced analytics and reporting
- 🔥 Custom branding and themes

## 📂 Project Structure

```
book-scraping-bot/
├── core/                   # Core scraping modules
│   ├── __init__.py
│   ├── scraper.py         # Main scraping logic
│   ├── downloader.py      # File download handler
│   └── metadata.py        # Metadata processing
├── uploaders/             # Upload modules
│   ├── __init__.py
│   ├── gdrive.py         # Google Drive uploader
│   └── ftp.py            # FTP uploader
├── enrichers/             # Data enrichment
│   ├── __init__.py
│   ├── books_api.py      # Google Books API
│   ├── openlibrary.py    # OpenLibrary API
│   └── affiliate.py      # Affiliate link generator
├── publishers/            # Content publishing
│   ├── __init__.py
│   ├── wordpress.py      # WordPress API
│   ├── blogspot.py       # Blogger API
│   └── static.py         # Static HTML generator
├── advanced/              # Premium features
│   ├── __init__.py
│   ├── video_gen.py      # Video generation
│   ├── telegram_bot.py   # Telegram notifications
│   └── analytics.py      # Analytics & reporting
├── config/                # Configuration
│   ├── __init__.py
│   ├── settings.py       # Main settings
│   └── credentials.py    # API credentials
├── templates/             # HTML templates
│   ├── book_page.html
│   └── book_list.html
├── output/                # Generated content
│   ├── metadata/
│   ├── covers/
│   ├── books/
│   └── html/
├── requirements.txt       # Dependencies
├── main.py               # Main entry point
└── README.md
```

## 🛠️ Installation

```bash
# Clone repository
git clone <your-repo-url>
cd book-scraping-bot

# Install dependencies
pip install -r requirements.txt

# Configure settings
cp config/settings.py.example config/settings.py
# Edit config/settings.py with your API keys
```

## 🚀 Quick Start

```python
from main import BookScrapingBot

# Initialize bot
bot = BookScrapingBot()

# Scrape a specific book
result = bot.scrape_book("clean code")

# Auto-process and upload
bot.process_and_upload(result)
```

## 💰 Monetization Features

- Amazon affiliate links
- eBay product links
- Google Books purchase links
- Custom affiliate tracking

## 🤖 Automation Features

- Scheduled scraping
- Auto-posting to CMS
- Social media content generation
- Email notifications

## 📊 Analytics (Premium)

- Download statistics
- Popular book tracking
- Revenue analytics
- Performance metrics

## 🔧 Configuration

Edit `config/settings.py` to customize:
- Scraping sources
- Upload destinations
- API credentials
- Publishing targets

## 📝 License

MIT License - Feel free to use and modify