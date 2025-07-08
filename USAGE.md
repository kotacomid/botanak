# 📚 Book Scraping Bot - Usage Guide

This guide shows you how to use the Book Scraping Bot effectively for both free and premium tiers.

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your API keys and settings
```

### Basic Usage

```bash
# Search for books
python main.py search "python programming"

# Search with limit
python main.py search "clean code" --limit 5

# Search without downloading
python main.py search "machine learning" --no-download

# Search specific source
python main.py search "algorithms" --source libgen
```

## 🔧 Configuration

### Environment Variables

Edit `.env` file to configure the bot:

```bash
# Enable premium features
IS_PREMIUM=true

# Download settings
DOWNLOAD_BOOKS=true
DOWNLOAD_COVERS=true
MAX_FILE_SIZE_MB=100

# Google Drive upload
GDRIVE_ENABLED=true
GDRIVE_FOLDER_ID=your_folder_id

# Affiliate monetization
AMAZON_AFFILIATE_TAG=your_tag
EBAY_AFFILIATE_ID=your_id
```

### API Keys Setup

1. **Google Drive API**:
   - Go to Google Cloud Console
   - Enable Drive API
   - Create credentials (OAuth2)
   - Download credentials.json
   - Place in `config/gdrive_credentials.json`

2. **Google Books API**:
   - Enable Books API in Google Cloud
   - Get API key
   - Set `GOOGLE_BOOKS_API_KEY` in .env

3. **Telegram Bot** (Premium):
   - Message @BotFather on Telegram
   - Create new bot
   - Get token and set `TELEGRAM_BOT_TOKEN`

## 📖 CLI Commands

### Search Commands

```bash
# Basic search
python main.py search "book title"

# Search specific book with author
python main.py book "Clean Code" --author "Robert Martin"

# Search from specific source
python main.py search "programming" --source annas-archive
```

### Management Commands

```bash
# Show statistics
python main.py stats

# Show configuration
python main.py config

# Clean up incomplete downloads
python main.py cleanup
```

## 🐍 Python API Usage

### Basic Scraping

```python
from main import BookScrapingBot

# Create bot instance
bot = BookScrapingBot()

# Search for books
results = bot.search_and_process("python programming", limit=10)

# Display results
bot.display_results(results)

# Close bot
bot.close()
```

### Advanced Usage

```python
from core import BookScraper, FileDownloader
from enrichers import AffiliateLinker

# Create components
scraper = BookScraper()
downloader = FileDownloader()
affiliate = AffiliateLinker()

# Search books
books = scraper.search_all_sources("machine learning", limit=5)

# Enrich with affiliate links
for book in books:
    affiliate.enrich_metadata(book)

# Download files
for book in books:
    if book.download_url:
        file_path = downloader.download_book(book)
        if file_path:
            book.local_file_path = file_path

# Close resources
scraper.close()
downloader.close()
```

### Async Downloads

```python
import asyncio
from main import BookScrapingBot

async def download_books():
    bot = BookScrapingBot()
    
    # Search books
    books = bot.search_and_process("programming", limit=10, download=False)
    
    # Download asynchronously
    results = await bot.downloader.download_multiple_async(books)
    
    print(f"Downloaded {len(results)} books")
    bot.close()

# Run async function
asyncio.run(download_books())
```

## 🔄 Automation & Scheduling

### Cron Job Example

```bash
# Add to crontab (crontab -e)
# Run every 6 hours
0 */6 * * * cd /path/to/bot && python main.py search "trending programming books" --limit 20

# Daily featured books
0 9 * * * cd /path/to/bot && python run_example.py
```

### Systemd Service

Create `/etc/systemd/system/bookbot.service`:

```ini
[Unit]
Description=Book Scraping Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 main.py search "daily books" --limit 50
Restart=always
RestartSec=3600

[Install]
WantedBy=multi-user.target
```

## 💰 Monetization Features

### Affiliate Links

The bot automatically generates affiliate links for:
- Amazon (requires affiliate tag)
- eBay (requires affiliate ID)
- Google Books
- Other book retailers

### Revenue Tracking

```python
from enrichers import AffiliateLinker

linker = AffiliateLinker()

# Track clicks for analytics
linker.track_click("book_id", "amazon")
```

## 🎥 Premium Features

### Video Generation

```python
# Premium feature
from advanced import VideoGenerator

if settings.IS_PREMIUM and settings.VIDEO_GENERATION_ENABLED:
    video_gen = VideoGenerator()
    
    for book in books:
        video_path = video_gen.create_book_video(book)
        if video_path:
            print(f"Generated video: {video_path}")
```

### Telegram Notifications

```python
from advanced import TelegramNotifier

if settings.TELEGRAM_BOT_ENABLED:
    notifier = TelegramNotifier()
    
    # Send new book notification
    notifier.send_book_notification(book)
```

### Analytics

```python
from advanced import AnalyticsTracker

if settings.ANALYTICS_ENABLED:
    analytics = AnalyticsTracker()
    
    # Track download
    analytics.track_download(book)
    
    # Get statistics
    stats = analytics.get_download_stats()
    print(f"Total downloads: {stats['total_downloads']}")
```

## 📊 Output Formats

### Generated Files

The bot creates several output formats:

```
output/
├── metadata/
│   ├── book_title.json      # Individual metadata
│   └── books.csv           # Combined CSV
├── books/
│   └── book_title.pdf      # Downloaded books
├── covers/
│   └── book_title.jpg      # Cover images
└── html/
    ├── book_title.html     # Individual pages
    ├── book_list.html      # List page
    ├── sitemap.xml         # SEO sitemap
    └── feed.xml           # RSS feed
```

### Metadata Format

JSON metadata includes:

```json
{
  "title": "Clean Code",
  "author": "Robert Martin",
  "isbn": "9780132350884",
  "year": 2008,
  "file_format": "PDF",
  "file_size": "10.2 MB",
  "download_url": "https://...",
  "amazon_link": "https://amazon.com/...",
  "local_file_path": "/path/to/file.pdf",
  "scraped_at": "2024-01-01T12:00:00",
  "source": "annas-archive"
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **No books found**:
   - Check internet connection
   - Try different search terms
   - Verify source websites are accessible

2. **Download failures**:
   - Check file size limits in config
   - Verify download URLs are valid
   - Check disk space

3. **API rate limits**:
   - Increase scraping delay
   - Use premium tier for higher limits
   - Add retry logic

### Debug Mode

```bash
# Enable debug logging
python main.py --debug search "test query"

# Or set in .env
DEBUG=true
```

### Validation

```bash
# Check configuration
python main.py config

# Validate setup
python -c "from config.settings import validate_config; print(validate_config())"
```

## 📈 Performance Tips

### Free Tier Optimization

- Use reasonable search limits (5-10 books)
- Enable selective downloads
- Cache results to avoid re-scraping
- Use built-in rate limiting

### Premium Tier Features

- Unlimited concurrent downloads
- Advanced video generation
- Real-time analytics
- Priority support
- Custom branding

### Memory Management

```python
# Process books in batches
def process_large_dataset(queries):
    for query in queries:
        bot = BookScrapingBot()
        results = bot.search_and_process(query, limit=20)
        # Process results...
        bot.close()  # Important: clean up resources
```

## 🤝 Contributing

See the main README.md for contribution guidelines.

## 📝 License

This project is licensed under the MIT License.

---

For more examples, see `run_example.py` in the project root.