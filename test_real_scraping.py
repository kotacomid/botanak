#!/usr/bin/env python3
"""
Real Scraping Test for Book Scraping Bot
Tests actual connections to Anna's Archive and LibGen
"""

import requests
import time
from bs4 import BeautifulSoup
import json
from pathlib import Path

def test_annas_archive():
    """Test real scraping from Anna's Archive"""
    print("🔍 Testing Anna's Archive...")
    
    try:
        # Real Anna's Archive search URL
        base_url = "https://annas-archive.org"
        search_query = "python programming"
        search_url = f"{base_url}/search?q={search_query}"
        
        print(f"📡 Connecting to: {search_url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        
        response = requests.get(search_url, headers=headers, timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Successfully connected to Anna's Archive")
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for different possible selectors
            print("🔍 Analyzing page structure...")
            
            # Try multiple selectors
            selectors_to_try = [
                'div[class*="mb-"]',  # Bootstrap-style classes
                'div[class*="result"]',
                'div[class*="book"]',
                'div[class*="item"]',
                'a[href*="/md5/"]',  # Direct links to books
                'a[href*="/book/"]',
                '.js-scroll-hidden'
            ]
            
            results_found = False
            for selector in selectors_to_try:
                elements = soup.select(selector)
                if elements:
                    print(f"✅ Found {len(elements)} elements with selector: {selector}")
                    
                    # Show first few results
                    for i, elem in enumerate(elements[:3]):
                        text = elem.get_text(strip=True)[:100]
                        print(f"   {i+1}. {text}...")
                    results_found = True
                    break
            
            if not results_found:
                print("❌ No results found with known selectors")
                # Save HTML for debugging
                debug_file = Path("debug_annas.html")
                debug_file.write_text(response.text, encoding='utf-8')
                print(f"💾 Saved HTML to {debug_file} for debugging")
            
            return results_found
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Anna's Archive: {e}")
        return False

def test_libgen():
    """Test real scraping from LibGen"""
    print("\n🔍 Testing LibGen...")
    
    try:
        # Try multiple LibGen mirrors
        libgen_urls = [
            "https://libgen.rs",
            "https://libgen.li", 
            "https://libgen.is"
        ]
        
        search_query = "python programming"
        
        for base_url in libgen_urls:
            print(f"📡 Trying {base_url}...")
            
            search_url = f"{base_url}/search.php?req={search_query}&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            
            try:
                response = requests.get(search_url, headers=headers, timeout=30)
                print(f"📊 Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"✅ Successfully connected to {base_url}")
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for LibGen results table
                    tables = soup.find_all('table')
                    print(f"🔍 Found {len(tables)} tables")
                    
                    results_found = False
                    for i, table in enumerate(tables):
                        rows = table.find_all('tr')
                        if len(rows) > 5:  # Likely results table
                            print(f"✅ Found results table {i+1} with {len(rows)} rows")
                            
                            # Show first few rows
                            for j, row in enumerate(rows[1:4]):  # Skip header
                                cells = row.find_all('td')
                                if len(cells) > 3:
                                    title = cells[2].get_text(strip=True) if len(cells) > 2 else "No title"
                                    author = cells[1].get_text(strip=True) if len(cells) > 1 else "No author"
                                    print(f"   📚 {title} by {author}")
                            results_found = True
                            break
                    
                    if results_found:
                        return True
                    else:
                        print("❌ No results table found")
                        # Save for debugging
                        debug_file = Path(f"debug_libgen_{base_url.split('//')[1].split('.')[0]}.html")
                        debug_file.write_text(response.text, encoding='utf-8')
                        print(f"💾 Saved HTML to {debug_file}")
                        
                else:
                    print(f"❌ HTTP Error: {response.status_code}")
                    
            except requests.RequestException as e:
                print(f"❌ Connection error to {base_url}: {e}")
                continue
        
        return False
        
    except Exception as e:
        print(f"❌ Error testing LibGen: {e}")
        return False

def test_simple_search():
    """Test a simple search that should work"""
    print("\n🧪 Testing simple search functionality...")
    
    # Test basic HTTP functionality
    try:
        print("📡 Testing basic HTTP...")
        response = requests.get("https://httpbin.org/get", timeout=10)
        if response.status_code == 200:
            print("✅ Basic HTTP works")
        else:
            print("❌ Basic HTTP failed")
            return False
    except Exception as e:
        print(f"❌ Basic HTTP error: {e}")
        return False
    
    # Test HTML parsing
    try:
        print("🔍 Testing HTML parsing...")
        html = "<html><body><div class='test'>Hello World</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        test_div = soup.find('div', class_='test')
        if test_div and test_div.get_text() == "Hello World":
            print("✅ HTML parsing works")
        else:
            print("❌ HTML parsing failed")
            return False
    except Exception as e:
        print(f"❌ HTML parsing error: {e}")
        return False
    
    return True

def create_working_scraper():
    """Create a working scraper based on real site analysis"""
    print("\n🔧 Creating working scraper...")
    
    scraper_code = '''"""
Working Book Scraper
Based on real site analysis
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from pathlib import Path

class WorkingBookScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
    
    def search_annas_archive(self, query, limit=10):
        """Search Anna's Archive with real working selectors"""
        try:
            url = f"https://annas-archive.org/search?q={query}"
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                print(f"Anna's Archive returned {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Updated selectors based on current site structure
            book_links = soup.find_all('a', href=True)
            
            for link in book_links[:limit]:
                href = link.get('href', '')
                if '/md5/' in href or '/book/' in href:
                    title = link.get_text(strip=True)
                    if title and len(title) > 10:  # Filter out navigation links
                        results.append({
                            'title': title,
                            'url': f"https://annas-archive.org{href}",
                            'source': 'annas-archive'
                        })
            
            return results[:limit]
            
        except Exception as e:
            print(f"Error searching Anna's Archive: {e}")
            return []
    
    def search_libgen(self, query, limit=10):
        """Search LibGen with working selectors"""
        libgen_mirrors = [
            "https://libgen.rs",
            "https://libgen.li"
        ]
        
        for mirror in libgen_mirrors:
            try:
                url = f"{mirror}/search.php"
                params = {
                    'req': query,
                    'lg_topic': 'libgen',
                    'open': '0',
                    'view': 'simple',
                    'res': '25',
                    'phrase': '1',
                    'column': 'def'
                }
                
                response = self.session.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find the main results table
                    tables = soup.find_all('table')
                    for table in tables:
                        rows = table.find_all('tr')
                        if len(rows) > 5:  # Main results table
                            results = []
                            
                            for row in rows[1:limit+1]:  # Skip header
                                cells = row.find_all('td')
                                if len(cells) >= 3:
                                    title = cells[2].get_text(strip=True)
                                    author = cells[1].get_text(strip=True) if len(cells) > 1 else ""
                                    
                                    if title:
                                        results.append({
                                            'title': title,
                                            'author': author,
                                            'source': 'libgen',
                                            'mirror': mirror
                                        })
                            
                            if results:
                                return results
                
            except Exception as e:
                print(f"Error with {mirror}: {e}")
                continue
        
        return []
    
    def search_all(self, query, limit=5):
        """Search all sources"""
        all_results = []
        
        print(f"🔍 Searching for: {query}")
        
        # Search Anna's Archive
        annas_results = self.search_annas_archive(query, limit)
        all_results.extend(annas_results)
        print(f"📚 Anna's Archive: {len(annas_results)} results")
        
        time.sleep(2)  # Be nice to servers
        
        # Search LibGen
        libgen_results = self.search_libgen(query, limit)
        all_results.extend(libgen_results)
        print(f"📚 LibGen: {len(libgen_results)} results")
        
        return all_results

# Test the working scraper
if __name__ == "__main__":
    scraper = WorkingBookScraper()
    results = scraper.search_all("python programming", limit=3)
    
    print(f"\\n✅ Total results: {len(results)}")
    
    if results:
        print("\\n📚 Found books:")
        for i, book in enumerate(results, 1):
            print(f"{i}. {book.get('title', 'No title')}")
            if book.get('author'):
                print(f"   Author: {book['author']}")
            print(f"   Source: {book['source']}")
            print()
        
        # Save results
        output_dir = Path("output/metadata")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results_file = output_dir / "working_test_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {results_file}")
    else:
        print("❌ No results found")
'''
    
    # Save the working scraper
    scraper_file = Path("working_scraper.py")
    scraper_file.write_text(scraper_code)
    print(f"✅ Working scraper saved to: {scraper_file}")
    
    return str(scraper_file)

def main():
    """Main test function"""
    print("🚀 Real Scraping Test for Book Bot")
    print("=" * 50)
    
    # Test basic functionality first
    if not test_simple_search():
        print("❌ Basic functionality failed")
        return
    
    # Test real sites
    annas_works = test_annas_archive()
    time.sleep(3)  # Be nice to servers
    libgen_works = test_libgen()
    
    print(f"\n📊 Test Results:")
    print(f"   Anna's Archive: {'✅ Working' if annas_works else '❌ Not working'}")
    print(f"   LibGen: {'✅ Working' if libgen_works else '❌ Not working'}")
    
    if annas_works or libgen_works:
        print("\n🔧 Creating working scraper...")
        scraper_file = create_working_scraper()
        print(f"\n🚀 Try the working scraper:")
        print(f"   python {scraper_file}")
    else:
        print("\n❌ Both sources failed. Possible issues:")
        print("   - Sites may be blocking requests")
        print("   - Network connectivity issues")
        print("   - Site structure may have changed")
        print("   - Geographic restrictions")
        
        print("\n💡 Troubleshooting suggestions:")
        print("   1. Check internet connection")
        print("   2. Try using VPN")
        print("   3. Update User-Agent string")
        print("   4. Check debug HTML files generated")

if __name__ == "__main__":
    main()