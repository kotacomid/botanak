#!/usr/bin/env python3
"""
Alternative Book Scraper
Uses stable public APIs when direct scraping fails
"""

import requests
import json
import time
from pathlib import Path

class AlternativeBookScraper:
    """Scraper using public APIs as backup"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Book-Scraper-Bot/1.0 (Educational Use)'
        })
    
    def search_openlibrary(self, query, limit=10):
        """Search OpenLibrary.org (free and open)"""
        print("🔍 Searching OpenLibrary...")
        
        try:
            url = "https://openlibrary.org/search.json"
            params = {
                'q': query,
                'limit': limit,
                'fields': 'key,title,author_name,first_publish_year,isbn,language,publisher,number_of_pages'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for book in data.get('docs', []):
                    title = book.get('title', 'Unknown Title')
                    authors = book.get('author_name', [])
                    author = authors[0] if authors else 'Unknown Author'
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
                        'source': 'openlibrary',
                        'url': f"https://openlibrary.org{book.get('key', '')}",
                        'available': True
                    }
                    
                    results.append(book_data)
                
                print(f"✅ OpenLibrary: Found {len(results)} books")
                return results
            else:
                print(f"❌ OpenLibrary API error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ OpenLibrary error: {e}")
            return []
    
    def search_google_books(self, query, limit=10, api_key=None):
        """Search Google Books API (free tier available)"""
        print("🔍 Searching Google Books...")
        
        try:
            url = "https://www.googleapis.com/books/v1/volumes"
            params = {
                'q': query,
                'maxResults': min(limit, 40),  # Google Books limit
                'printType': 'books'
            }
            
            if api_key:
                params['key'] = api_key
            
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
                    
                    book_data = {
                        'title': title,
                        'author': author,
                        'year': volume_info.get('publishedDate', '').split('-')[0] if volume_info.get('publishedDate') else None,
                        'isbn': isbn,
                        'publisher': volume_info.get('publisher', ''),
                        'pages': volume_info.get('pageCount'),
                        'language': volume_info.get('language', ''),
                        'description': volume_info.get('description', ''),
                        'source': 'google_books',
                        'url': volume_info.get('infoLink', ''),
                        'preview_link': volume_info.get('previewLink', ''),
                        'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                        'available': True
                    }
                    
                    results.append(book_data)
                
                print(f"✅ Google Books: Found {len(results)} books")
                return results
            else:
                print(f"❌ Google Books API error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Google Books error: {e}")
            return []
    
    def search_internet_archive(self, query, limit=10):
        """Search Internet Archive (archive.org)"""
        print("🔍 Searching Internet Archive...")
        
        try:
            url = "https://archive.org/advancedsearch.php"
            params = {
                'q': f'title:({query}) AND mediatype:texts',
                'fl': 'identifier,title,creator,date,publisher,description,downloads',
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
                        creator = ', '.join(creator)
                    
                    identifier = doc.get('identifier', '')
                    
                    book_data = {
                        'title': title,
                        'author': creator,
                        'year': doc.get('date'),
                        'publisher': doc.get('publisher', ''),
                        'description': doc.get('description', ''),
                        'downloads': doc.get('downloads', 0),
                        'source': 'internet_archive',
                        'url': f"https://archive.org/details/{identifier}",
                        'download_url': f"https://archive.org/download/{identifier}",
                        'available': True
                    }
                    
                    results.append(book_data)
                
                print(f"✅ Internet Archive: Found {len(results)} books")
                return results
            else:
                print(f"❌ Internet Archive error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Internet Archive error: {e}")
            return []
    
    def search_all_sources(self, query, limit_per_source=5):
        """Search all available sources"""
        all_results = []
        
        print(f"🚀 Searching for: '{query}'")
        print("=" * 40)
        
        # Search OpenLibrary
        openlibrary_results = self.search_openlibrary(query, limit_per_source)
        all_results.extend(openlibrary_results)
        time.sleep(1)  # Be nice to APIs
        
        # Search Google Books
        google_results = self.search_google_books(query, limit_per_source)
        all_results.extend(google_results)
        time.sleep(1)
        
        # Search Internet Archive
        archive_results = self.search_internet_archive(query, limit_per_source)
        all_results.extend(archive_results)
        
        return all_results
    
    def create_book_html(self, book):
        """Create HTML page for a book"""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{book['title']} by {book['author']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            background: #f5f5f5;
        }}
        .book-card {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #2c3e50; margin-bottom: 10px; }}
        .author {{ color: #7f8c8d; font-size: 1.2em; margin-bottom: 20px; }}
        .meta {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .meta-item {{ margin: 5px 0; }}
        .description {{ margin: 20px 0; }}
        .links {{ margin: 20px 0; }}
        .btn {{
            display: inline-block;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 5px;
        }}
        .btn:hover {{ background: #2980b9; }}
        .source {{ color: #e74c3c; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="book-card">
        <h1>{book['title']}</h1>
        <div class="author">by {book['author']}</div>
        
        <div class="meta">
            <div class="meta-item"><strong>Source:</strong> <span class="source">{book['source'].replace('_', ' ').title()}</span></div>
            {f'<div class="meta-item"><strong>Year:</strong> {book["year"]}</div>' if book.get('year') else ''}
            {f'<div class="meta-item"><strong>Publisher:</strong> {book["publisher"]}</div>' if book.get('publisher') else ''}
            {f'<div class="meta-item"><strong>Pages:</strong> {book["pages"]}</div>' if book.get('pages') else ''}
            {f'<div class="meta-item"><strong>ISBN:</strong> {book["isbn"]}</div>' if book.get('isbn') else ''}
            {f'<div class="meta-item"><strong>Language:</strong> {book["language"]}</div>' if book.get('language') else ''}
        </div>
        
        {f'<div class="description"><h3>Description</h3><p>{book["description"][:500]}...</p></div>' if book.get('description') else ''}
        
        <div class="links">
            <h3>Links</h3>
            {f'<a href="{book["url"]}" class="btn" target="_blank">View Details</a>' if book.get('url') else ''}
            {f'<a href="{book["preview_link"]}" class="btn" target="_blank">Preview</a>' if book.get('preview_link') else ''}
            {f'<a href="{book["download_url"]}" class="btn" target="_blank">Download</a>' if book.get('download_url') else ''}
        </div>
    </div>
</body>
</html>"""
        
        return html_content
    
    def save_results(self, results, query):
        """Save results to files"""
        if not results:
            return
        
        # Create output directories
        output_dir = Path("output")
        metadata_dir = output_dir / "metadata"
        html_dir = output_dir / "html"
        
        metadata_dir.mkdir(parents=True, exist_ok=True)
        html_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSON metadata
        json_file = metadata_dir / f"search_{query.replace(' ', '_')}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved metadata: {json_file}")
        
        # Save HTML pages
        for i, book in enumerate(results):
            filename = f"{query.replace(' ', '_')}_book_{i+1}.html"
            html_file = html_dir / filename
            
            html_content = self.create_book_html(book)
            html_file.write_text(html_content, encoding='utf-8')
        
        print(f"🌐 Saved {len(results)} HTML pages to {html_dir}")
        
        return str(json_file)

def main():
    """Test the alternative scraper"""
    print("🚀 Alternative Book Scraper Test")
    print("=" * 40)
    
    scraper = AlternativeBookScraper()
    
    # Test queries
    test_queries = [
        "python programming",
        "machine learning", 
        "data science"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing query: '{query}'")
        results = scraper.search_all_sources(query, limit_per_source=3)
        
        if results:
            print(f"\n✅ Found {len(results)} total books for '{query}':")
            
            # Group by source
            by_source = {}
            for book in results:
                source = book['source']
                if source not in by_source:
                    by_source[source] = []
                by_source[source].append(book)
            
            for source, books in by_source.items():
                print(f"\n📚 {source.replace('_', ' ').title()} ({len(books)} books):")
                for book in books[:2]:  # Show first 2 from each source
                    print(f"   • {book['title']} by {book['author']}")
            
            # Save results
            scraper.save_results(results, query)
        else:
            print(f"❌ No results found for '{query}'")
        
        time.sleep(2)  # Be nice to APIs
    
    print("\n🎉 Alternative scraper test completed!")
    print("📂 Check output/ folder for generated files")

if __name__ == "__main__":
    main()