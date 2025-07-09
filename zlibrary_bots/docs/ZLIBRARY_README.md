# 📚 Simple and Powerful Z-Library Bot

A clean, easy-to-use interface for the Z-Library Python package with comprehensive functionality for searching and accessing books.

## 🚀 Features

### ✅ Core Features
- **Simple Interface**: Clean, intuitive API for Z-Library access
- **Multiple Search Types**: Basic, advanced, and full-text search
- **Authentication Support**: Optional login for enhanced features
- **Filter Support**: Year range, language, file format filtering
- **Result Management**: Save results as JSON, display formatted output
- **Async/Await**: Modern async Python for better performance
- **Error Handling**: Robust error handling with user-friendly messages

### 🔧 Advanced Features
- **Download Limits**: Check your account download limits
- **Download History**: Access your download history
- **Proxy Support**: Tor/onion network support for privacy
- **Pagination**: Handle large result sets efficiently
- **Result Caching**: Efficient result management

## 📦 Installation

1. **Install the zlibrary package:**
   ```bash
   pip install zlibrary
   ```

2. **Install additional dependencies (if using the full bot):**
   ```bash
   pip install rich click
   ```

## 🏃‍♂️ Quick Start

### Basic Usage (No Authentication Required)

```python
import asyncio
from zlibrary_example import SimpleZLibrary

async def main():
    async with SimpleZLibrary() as zlib:
        # Search for books
        results = await zlib.search("python programming", count=5)
        
        # Display results
        zlib.print_results(results)
        
        # Save results
        zlib.save_results(results, "my_search.json")

asyncio.run(main())
```

### With Authentication (Enhanced Features)

```python
import asyncio
from zlibrary_example import SimpleZLibrary

async def main():
    # Replace with your Z-Library credentials
    email = "your_email@example.com"
    password = "your_password"
    
    async with SimpleZLibrary(email, password) as zlib:
        # Check download limits
        limits = await zlib.get_limits()
        print(f"Daily downloads remaining: {limits.get('daily_remaining', 'Unknown')}")
        
        # Search with authentication
        results = await zlib.search("machine learning", count=10)
        zlib.print_results(results)

asyncio.run(main())
```

## 📖 Usage Examples

### 1. Basic Search

```python
async def basic_search_example():
    async with SimpleZLibrary() as zlib:
        results = await zlib.search("artificial intelligence", count=10)
        zlib.print_results(results)
        zlib.save_results(results, "ai_books.json")
```

### 2. Advanced Search with Filters

```python
async def advanced_search_example():
    async with SimpleZLibrary() as zlib:
        results = await zlib.search_advanced(
            query="data science",
            count=15,
            from_year=2020,
            to_year=2024,
            language="english",
            file_format="pdf"
        )
        zlib.print_results(results)
```

### 3. Full-Text Search

```python
async def fulltext_search_example():
    async with SimpleZLibrary() as zlib:
        # Search inside book contents
        results = await zlib.full_text_search(
            "neural networks and backpropagation",
            exact_phrase=True
        )
        zlib.print_results(results)
```

### 4. Multiple Topic Search

```python
async def multi_topic_search():
    async with SimpleZLibrary() as zlib:
        topics = ["web development", "mobile apps", "cloud computing"]
        all_results = []
        
        for topic in topics:
            results = await zlib.search(topic, count=5)
            all_results.extend(results)
            
        zlib.save_results(all_results, "tech_books.json")
        print(f"Total books found: {len(all_results)}")
```

## 🎛️ Command Line Interface

The `zlibrary_bot.py` provides a full CLI interface:

### Basic Commands

```bash
# Search for books
python zlibrary_bot.py search "python programming" --count 10

# Advanced search with filters
python zlibrary_bot.py search "machine learning" \
    --from-year 2020 \
    --language english \
    --format pdf \
    --save json

# Full-text search
python zlibrary_bot.py fulltext "deep learning algorithms" --phrase

# Interactive mode
python zlibrary_bot.py interactive
```

### With Authentication

```bash
# Use with credentials
python zlibrary_bot.py --email your@email.com --password your_pass search "data science"

# Check download limits
python zlibrary_bot.py --email your@email.com --password your_pass limits

# View download history
python zlibrary_bot.py --email your@email.com --password your_pass history
```

### Privacy/Tor Support

```bash
# Use with Tor (requires tor service running)
python zlibrary_bot.py --onion --proxy socks5://127.0.0.1:9050 search "programming"
```

## 🔧 Configuration Options

### Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `query` | string | Search term | "python programming" |
| `count` | integer | Number of results | 10 |
| `from_year` | integer | Start year filter | 2020 |
| `to_year` | integer | End year filter | 2024 |
| `language` | string | Language filter | "english", "russian" |
| `file_format` | string | File format filter | "pdf", "epub", "mobi" |

### Supported Languages

- English (`english`)
- Russian (`russian`)
- German (`german`)
- French (`french`)
- Spanish (`spanish`)
- Italian (`italian`)
- Chinese (`chinese`)
- Japanese (`japanese`)

### Supported File Formats

- PDF (`pdf`)
- EPUB (`epub`)
- MOBI (`mobi`)
- AZW (`azw`)
- AZW3 (`azw3`)
- FB2 (`fb2`)
- TXT (`txt`)
- RTF (`rtf`)
- DOC (`doc`)
- DOCX (`docx`)

## 📁 Output Structure

The bot creates organized output in the `zlibrary_output` directory:

```
zlibrary_output/
├── books/           # Downloaded book files
├── covers/          # Downloaded cover images
└── metadata/        # Search results in JSON/CSV format
    ├── books_20240101_120000.json
    ├── python_books.json
    └── tech_books.json
```

## 🛡️ Privacy and Security

### Tor/Onion Support

```python
async def tor_example():
    # Use with Tor for privacy
    async with SimpleZLibrary() as zlib:
        zlib.use_onion = True
        zlib.proxy_list = ['socks5://127.0.0.1:9050']
        
        results = await zlib.search("privacy books")
        zlib.print_results(results)
```

### Setting up Tor (Linux)

```bash
# Install Tor
sudo apt install tor obfs4proxy

# Start Tor service
sudo systemctl enable --now tor

# For countries with Tor blocks, configure bridges in /etc/tor/torrc
```

## 🎯 Advanced Usage

### Custom Result Processing

```python
async def custom_processing():
    async with SimpleZLibrary() as zlib:
        results = await zlib.search("machine learning")
        
        # Filter by rating
        high_rated = [book for book in results 
                     if book.get('rating', '0').startswith(('4', '5'))]
        
        # Filter by recent books
        recent_books = [book for book in results 
                       if book.get('year', '0') >= '2020']
        
        print(f"High rated books: {len(high_rated)}")
        print(f"Recent books: {len(recent_books)}")
```

### Batch Processing

```python
async def batch_processing():
    search_queries = [
        "python programming",
        "javascript development", 
        "data science",
        "machine learning",
        "artificial intelligence"
    ]
    
    async with SimpleZLibrary() as zlib:
        all_results = {}
        
        for query in search_queries:
            results = await zlib.search(query, count=5)
            all_results[query] = results
            
        # Save categorized results
        for topic, books in all_results.items():
            filename = f"{topic.replace(' ', '_')}_books.json"
            zlib.save_results(books, filename)
```

## 🤝 Integration with Existing Bot

To integrate with your existing book scraping bot, add Z-Library as a source:

```python
# In your main bot
from zlibrary_example import SimpleZLibrary

class BookScrapingBot:
    def __init__(self):
        # ... existing code ...
        self.zlibrary = None
    
    async def search_zlibrary(self, query: str, count: int = 10):
        """Add Z-Library search to your bot"""
        if not self.zlibrary:
            self.zlibrary = SimpleZLibrary()
            await self.zlibrary.connect()
        
        return await self.zlibrary.search(query, count)
```

## 📊 Error Handling

The bot includes comprehensive error handling:

```python
async def robust_search():
    try:
        async with SimpleZLibrary("email", "password") as zlib:
            results = await zlib.search("programming")
            
            if not results:
                print("No results found")
                return
                
            zlib.print_results(results)
            
    except RuntimeError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

## 🚀 Running the Examples

1. **Run the simple examples:**
   ```bash
   python zlibrary_example.py
   ```

2. **Run specific examples:**
   ```python
   import asyncio
   from zlibrary_example import example_basic_search
   
   asyncio.run(example_basic_search())
   ```

3. **Use the CLI interface:**
   ```bash
   python zlibrary_bot.py interactive
   ```

## 🔗 Useful Links

- [Z-Library Official](https://zlibrary.to)
- [zlibrary Python Package](https://pypi.org/project/zlibrary/)
- [Tor Project](https://www.torproject.org/)

## ⚠️ Legal Notice

This tool is for educational and personal use only. Please respect copyright laws and Z-Library's terms of service. Only download books you have the right to access.

## 🤝 Contributing

Feel free to improve this implementation by:
- Adding more search filters
- Improving error handling
- Adding download functionality
- Enhancing the CLI interface
- Adding more output formats

## 📄 License

This implementation is provided as-is for educational purposes. Please comply with all applicable laws and terms of service.