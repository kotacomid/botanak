#!/usr/bin/env python3
"""
Enhanced Production-Ready Book Scraping Bot
Combines all working sources for maximum data collection
"""

import requests
import json
import time
import re
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import quote_plus, urljoin
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedBookBot:
    """Enhanced book scraping bot with multiple sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        self.results = []
    
    def search_annas_archive_enhanced(self, query, limit=10):
        """Enhanced Anna's Archive scraping with better selectors"""
        logger.info(f"🔍 Searching Anna's Archive for: {query}")
        
        try:
            url = f"https://annas-archive.org/search?q={quote_plus(query)}"
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                logger.warning(f"Anna's Archive returned {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Multiple selector strategies
            selectors = [
                # Look for book links in results
                'a[href*="/md5/"]',
                'a[href*="/book/"]',
                # Look for results containers
                '.js-scroll-hidden a',
                '.mb-2 a',
                '.mb-3 a',
                # Text patterns that indicate book results
                'div:contains("MB")',
                'div:contains("PDF")',
                'div:contains("EPUB")'
            ]
            
            found_links = set()
            
            for selector in selectors:
                try:
                    elements = soup.select(selector)
                    for elem in elements:
                        href = elem.get('href', '') or ''
                        text = elem.get_text(strip=True)
                        
                        # Filter valid book links
                        if (href and ('/md5/' in href or '/book/' in href) and 
                            len(text) > 10 and 
                            not any(skip in text.lower() for skip in ['search', 'donate', 'mirror'])):
                            
                            if href not in found_links:
                                found_links.add(href)
                                
                                # Extract metadata from surrounding elements
                                parent = elem.parent
                                metadata = self._extract_annas_metadata(elem, parent)
                                
                                book_data = {
                                    'title': text,
                                    'author': metadata.get('author', 'Unknown Author'),
                                    'year': metadata.get('year'),
                                    'filesize': metadata.get('filesize'),
                                    'filetype': metadata.get('filetype'),
                                    'source': 'annas_archive',
                                    'url': f"https://annas-archive.org{href}",
                                    'available': True
                                }
                                
                                results.append(book_data)
                                
                                if len(results) >= limit:
                                    break
                    
                    if results:
                        break
                        
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            logger.info(f"✅ Anna's Archive: Found {len(results)} books")
            return results
            
        except Exception as e:
            logger.error(f"❌ Anna's Archive error: {e}")
            return []
    
    def _extract_annas_metadata(self, element, parent):
        """Extract metadata from Anna's Archive page structure"""
        metadata = {}
        
        try:
            # Look for patterns in surrounding text
            full_text = parent.get_text() if parent else element.get_text()
            
            # Extract file size (e.g., "1.2MB", "500KB")
            size_match = re.search(r'(\d+(?:\.\d+)?)\s*(MB|KB|GB)', full_text, re.IGNORECASE)
            if size_match:
                metadata['filesize'] = f"{size_match.group(1)}{size_match.group(2)}"
            
            # Extract file type (PDF, EPUB, etc.)
            type_match = re.search(r'\b(PDF|EPUB|MOBI|AZW3|TXT)\b', full_text, re.IGNORECASE)
            if type_match:
                metadata['filetype'] = type_match.group(1).upper()
            
            # Extract year
            year_match = re.search(r'\b(19|20)\d{2}\b', full_text)
            if year_match:
                metadata['year'] = int(year_match.group())
            
            # Extract author from patterns like "by Author Name"
            author_match = re.search(r'\bby\s+([^,\n]+)', full_text, re.IGNORECASE)
            if author_match:
                metadata['author'] = author_match.group(1).strip()
            
        except Exception as e:
            logger.debug(f"Metadata extraction error: {e}")
        
        return metadata
    
    def search_openlibrary(self, query, limit=10):
        """Search OpenLibrary.org"""
        logger.info(f"🔍 Searching OpenLibrary for: {query}")
        
        try:
            url = "https://openlibrary.org/search.json"
            params = {
                'q': query,
                'limit': limit,
                'fields': 'key,title,author_name,first_publish_year,isbn,language,publisher,number_of_pages,subject'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for book in data.get('docs', []):
                    title = book.get('title', 'Unknown Title')
                    authors = book.get('author_name', [])
                    author = ', '.join(authors[:2]) if authors else 'Unknown Author'
                    year = book.get('first_publish_year')
                    isbn_list = book.get('isbn', [])
                    isbn = isbn_list[0] if isbn_list else ''
                    
                    book_data = {
                        'title': title,
                        'author': author,
                        'year': year,
                        'isbn': isbn,
                        'publisher': book.get('publisher', [''])[0] if book.get('publisher') else '',
                        'pages': book.get('number_of_pages'),
                        'language': book.get('language', [''])[0] if book.get('language') else '',
                        'subjects': book.get('subject', [])[:5],  # First 5 subjects
                        'source': 'openlibrary',
                        'url': f"https://openlibrary.org{book.get('key', '')}",
                        'available': True
                    }
                    
                    results.append(book_data)
                
                logger.info(f"✅ OpenLibrary: Found {len(results)} books")
                return results
            else:
                logger.warning(f"❌ OpenLibrary API error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ OpenLibrary error: {e}")
            return []
    
    def search_google_books(self, query, limit=10):
        """Search Google Books API"""
        logger.info(f"🔍 Searching Google Books for: {query}")
        
        try:
            url = "https://www.googleapis.com/books/v1/volumes"
            params = {
                'q': query,
                'maxResults': min(limit, 40),
                'printType': 'books'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get('items', []):
                    volume_info = item.get('volumeInfo', {})
                    
                    title = volume_info.get('title', 'Unknown Title')
                    authors = volume_info.get('authors', [])
                    author = ', '.join(authors) if authors else 'Unknown Author'
                    
                    # Get identifiers
                    identifiers = volume_info.get('industryIdentifiers', [])
                    isbn = ''
                    for identifier in identifiers:
                        if identifier.get('type') in ['ISBN_13', 'ISBN_10']:
                            isbn = identifier.get('identifier', '')
                            break
                    
                    # Extract categories
                    categories = volume_info.get('categories', [])
                    
                    book_data = {
                        'title': title,
                        'author': author,
                        'year': volume_info.get('publishedDate', '').split('-')[0] if volume_info.get('publishedDate') else None,
                        'isbn': isbn,
                        'publisher': volume_info.get('publisher', ''),
                        'pages': volume_info.get('pageCount'),
                        'language': volume_info.get('language', ''),
                        'description': volume_info.get('description', '')[:500],  # First 500 chars
                        'categories': categories[:3],  # First 3 categories
                        'rating': volume_info.get('averageRating'),
                        'source': 'google_books',
                        'url': volume_info.get('infoLink', ''),
                        'preview_link': volume_info.get('previewLink', ''),
                        'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                        'available': True
                    }
                    
                    results.append(book_data)
                
                logger.info(f"✅ Google Books: Found {len(results)} books")
                return results
            else:
                logger.warning(f"❌ Google Books API error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Google Books error: {e}")
            return []
    
    def search_internet_archive(self, query, limit=10):
        """Search Internet Archive"""
        logger.info(f"🔍 Searching Internet Archive for: {query}")
        
        try:
            url = "https://archive.org/advancedsearch.php"
            params = {
                'q': f'title:({query}) AND mediatype:texts',
                'fl': 'identifier,title,creator,date,publisher,description,downloads,format',
                'rows': limit,
                'page': 1,
                'output': 'json'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for doc in data.get('response', {}).get('docs', []):
                    title = doc.get('title', 'Unknown Title')
                    if isinstance(title, list):
                        title = title[0]
                    
                    creator = doc.get('creator', 'Unknown Author')
                    if isinstance(creator, list):
                        creator = ', '.join(creator[:2])  # First 2 creators
                    
                    identifier = doc.get('identifier', '')
                    formats = doc.get('format', [])
                    
                    book_data = {
                        'title': title,
                        'author': creator,
                        'year': doc.get('date'),
                        'publisher': doc.get('publisher', ''),
                        'description': doc.get('description', '')[:300] if doc.get('description') else '',
                        'downloads': doc.get('downloads', 0),
                        'formats': formats[:5] if isinstance(formats, list) else [],
                        'source': 'internet_archive',
                        'url': f"https://archive.org/details/{identifier}",
                        'download_url': f"https://archive.org/download/{identifier}",
                        'available': True
                    }
                    
                    results.append(book_data)
                
                logger.info(f"✅ Internet Archive: Found {len(results)} books")
                return results
            else:
                logger.warning(f"❌ Internet Archive error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Internet Archive error: {e}")
            return []
    
    def search_all_sources(self, query, limit_per_source=5):
        """Search all sources and combine results"""
        logger.info(f"🚀 Starting comprehensive search for: '{query}'")
        logger.info("=" * 50)
        
        all_results = []
        
        # Search all sources in parallel concept (sequential for now due to rate limiting)
        sources = [
            ('annas_archive', self.search_annas_archive_enhanced),
            ('openlibrary', self.search_openlibrary),
            ('google_books', self.search_google_books),
            ('internet_archive', self.search_internet_archive)
        ]
        
        for source_name, search_func in sources:
            try:
                results = search_func(query, limit_per_source)
                all_results.extend(results)
                
                # Be nice to APIs
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error with {source_name}: {e}")
                continue
        
        # Remove duplicates based on title similarity
        unique_results = self._remove_duplicates(all_results)
        
        logger.info(f"🎉 Total unique books found: {len(unique_results)}")
        
        return unique_results
    
    def _remove_duplicates(self, results):
        """Remove duplicate books based on title similarity"""
        unique_books = []
        seen_titles = set()
        
        for book in results:
            title_normalized = re.sub(r'[^\w\s]', '', book['title'].lower())
            title_words = set(title_normalized.split())
            
            # Check similarity with existing titles
            is_duplicate = False
            for seen_title in seen_titles:
                seen_words = set(seen_title.split())
                
                # If significant word overlap, consider duplicate
                if len(title_words & seen_words) / max(len(title_words), len(seen_words)) > 0.7:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                seen_titles.add(title_normalized)
                unique_books.append(book)
        
        logger.info(f"🧹 Removed {len(results) - len(unique_books)} duplicates")
        return unique_books
    
    def generate_enhanced_html(self, books, query):
        """Generate enhanced HTML with better styling"""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Book Search Results: {query}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.2em; opacity: 0.9; }}
        .stats {{
            display: flex;
            justify-content: space-around;
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #eee;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }}
        .stat-label {{
            color: #7f8c8d;
            margin-top: 5px;
        }}
        .books-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            padding: 30px;
        }}
        .book-card {{
            border: 1px solid #e1e8ed;
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s ease;
            background: white;
        }}
        .book-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-color: #3498db;
        }}
        .book-header {{
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
        }}
        .book-thumbnail {{
            width: 80px;
            height: 120px;
            background: #f8f9fa;
            border-radius: 5px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #bdc3c7;
            font-size: 0.8em;
            text-align: center;
            flex-shrink: 0;
        }}
        .book-thumbnail img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 5px;
        }}
        .book-info {{
            flex: 1;
        }}
        .book-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
            line-height: 1.3;
        }}
        .book-author {{
            color: #7f8c8d;
            font-size: 1.1em;
            margin-bottom: 10px;
        }}
        .book-meta {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }}
        .meta-item {{
            background: #f8f9fa;
            padding: 8px 12px;
            border-radius: 5px;
            font-size: 0.9em;
        }}
        .meta-label {{
            font-weight: bold;
            color: #34495e;
        }}
        .source-badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: bold;
            color: white;
            margin: 5px 0;
        }}
        .source-annas_archive {{ background: #e74c3c; }}
        .source-openlibrary {{ background: #2ecc71; }}
        .source-google_books {{ background: #3498db; }}
        .source-internet_archive {{ background: #f39c12; }}
        .book-actions {{
            margin-top: 15px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .btn {{
            padding: 8px 15px;
            border: none;
            border-radius: 5px;
            text-decoration: none;
            font-size: 0.9em;
            font-weight: bold;
            transition: all 0.3s ease;
            display: inline-block;
        }}
        .btn-primary {{
            background: #3498db;
            color: white;
        }}
        .btn-primary:hover {{
            background: #2980b9;
        }}
        .btn-secondary {{
            background: #95a5a6;
            color: white;
        }}
        .btn-secondary:hover {{
            background: #7f8c8d;
        }}
        .description {{
            margin-top: 15px;
            color: #555;
            line-height: 1.6;
            font-size: 0.95em;
        }}
        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Book Search Results</h1>
            <p>Search query: "{query}"</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number">{len(books)}</div>
                <div class="stat-label">Total Books</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len(set(book['source'] for book in books))}</div>
                <div class="stat-label">Sources</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len([b for b in books if b.get('year')])}</div>
                <div class="stat-label">With Year</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len([b for b in books if b.get('isbn')])}</div>
                <div class="stat-label">With ISBN</div>
            </div>
        </div>
        
        <div class="books-grid">"""
        
        for book in books:
            thumbnail_html = ""
            if book.get('thumbnail'):
                thumbnail_html = f'<img src="{book["thumbnail"]}" alt="Book cover">'
            else:
                thumbnail_html = "No Cover"
            
            description_html = ""
            if book.get('description'):
                description_html = f'<div class="description">{book["description"][:200]}...</div>'
            
            actions_html = ""
            if book.get('url'):
                actions_html += f'<a href="{book["url"]}" class="btn btn-primary" target="_blank">View Details</a>'
            if book.get('preview_link'):
                actions_html += f'<a href="{book["preview_link"]}" class="btn btn-secondary" target="_blank">Preview</a>'
            if book.get('download_url'):
                actions_html += f'<a href="{book["download_url"]}" class="btn btn-primary" target="_blank">Download</a>'
            
            html_content += f"""
            <div class="book-card">
                <div class="book-header">
                    <div class="book-thumbnail">{thumbnail_html}</div>
                    <div class="book-info">
                        <div class="book-title">{book['title']}</div>
                        <div class="book-author">by {book['author']}</div>
                        <span class="source-badge source-{book['source']}">{book['source'].replace('_', ' ').title()}</span>
                    </div>
                </div>
                
                <div class="book-meta">
                    {f'<div class="meta-item"><span class="meta-label">Year:</span> {book["year"]}</div>' if book.get('year') else ''}
                    {f'<div class="meta-item"><span class="meta-label">Pages:</span> {book["pages"]}</div>' if book.get('pages') else ''}
                    {f'<div class="meta-item"><span class="meta-label">ISBN:</span> {book["isbn"]}</div>' if book.get('isbn') else ''}
                    {f'<div class="meta-item"><span class="meta-label">Publisher:</span> {book["publisher"]}</div>' if book.get('publisher') else ''}
                    {f'<div class="meta-item"><span class="meta-label">Language:</span> {book["language"]}</div>' if book.get('language') else ''}
                    {f'<div class="meta-item"><span class="meta-label">Downloads:</span> {book["downloads"]}</div>' if book.get('downloads') else ''}
                </div>
                
                {description_html}
                
                <div class="book-actions">
                    {actions_html}
                </div>
            </div>"""
        
        html_content += """
        </div>
        
        <div class="footer">
            <p>Generated by Enhanced Book Scraping Bot | Data sources: Anna's Archive, OpenLibrary, Google Books, Internet Archive</p>
        </div>
    </div>
</body>
</html>"""
        
        return html_content
    
    def save_results(self, results, query):
        """Save results to JSON and HTML"""
        if not results:
            logger.warning("No results to save")
            return
        
        # Create directories
        output_dir = Path("output")
        metadata_dir = output_dir / "metadata" 
        html_dir = output_dir / "html"
        
        metadata_dir.mkdir(parents=True, exist_ok=True)
        html_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSON metadata
        timestamp = int(time.time())
        json_file = metadata_dir / f"enhanced_search_{query.replace(' ', '_')}_{timestamp}.json"
        
        # Add search metadata
        search_metadata = {
            'query': query,
            'timestamp': timestamp,
            'total_results': len(results),
            'sources_used': list(set(book['source'] for book in results)),
            'books': results
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(search_metadata, f, indent=2, ensure_ascii=False)
        
        # Save HTML
        html_file = html_dir / f"enhanced_search_{query.replace(' ', '_')}_{timestamp}.html"
        html_content = self.generate_enhanced_html(results, query)
        html_file.write_text(html_content, encoding='utf-8')
        
        logger.info(f"💾 Results saved:")
        logger.info(f"   📄 JSON: {json_file}")
        logger.info(f"   🌐 HTML: {html_file}")
        
        return str(json_file), str(html_file)

def main():
    """Enhanced bot demonstration"""
    print("🚀 Enhanced Book Scraping Bot")
    print("=" * 50)
    
    bot = EnhancedBookBot()
    
    # Test queries
    test_queries = [
        "python programming",
        "machine learning artificial intelligence",
        "data science statistics"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing enhanced search: '{query}'")
        
        results = bot.search_all_sources(query, limit_per_source=3)
        
        if results:
            # Group by source for display
            by_source = {}
            for book in results:
                source = book['source']
                if source not in by_source:
                    by_source[source] = []
                by_source[source].append(book)
            
            print(f"\n✅ Found {len(results)} unique books:")
            for source, books in by_source.items():
                print(f"\n📚 {source.replace('_', ' ').title()} ({len(books)} books):")
                for book in books[:2]:  # Show first 2
                    year_info = f" ({book['year']})" if book.get('year') else ""
                    print(f"   • {book['title']} by {book['author']}{year_info}")
            
            # Save results
            json_file, html_file = bot.save_results(results, query)
            print(f"\n💾 Results saved to files")
        else:
            print(f"❌ No results found for '{query}'")
        
        print("\n" + "="*50)
        time.sleep(2)
    
    print("\n🎉 Enhanced bot testing completed!")
    print("📂 Check the output/ directory for all generated files")

if __name__ == "__main__":
    main()