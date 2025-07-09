"""
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
    
    print(f"\n✅ Total results: {len(results)}")
    
    if results:
        print("\n📚 Found books:")
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
