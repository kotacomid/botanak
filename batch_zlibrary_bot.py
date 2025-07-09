#!/usr/bin/env python3
"""
Batch Z-Library Bot
Individual bot for batch processing multiple searches
"""

import asyncio
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict

def check_zlibrary():
    """Check zlibrary availability"""
    try:
        import zlibrary
        from zlibrary import Language, Extension
        print("✅ zlibrary available")
        return True, zlibrary, Language, Extension
    except ImportError:
        print("❌ zlibrary not available")
        print("Install: pip install zlibrary")
        return False, None, None, None

class BatchZBot:
    """Batch processing Z-Library bot"""
    
    def __init__(self):
        """Initialize batch bot"""
        self.available, self.zlibrary, self.Language, self.Extension = check_zlibrary()
        self.lib = None
        self.results_dir = Path("batch_zlibrary_results")
        self.results_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.results_dir / "json").mkdir(exist_ok=True)
        (self.results_dir / "csv").mkdir(exist_ok=True)
        (self.results_dir / "reports").mkdir(exist_ok=True)
        
        print(f"📁 Batch results: {self.results_dir}")
    
    async def connect(self, email=None, password=None):
        """Connect to Z-Library"""
        if not self.available:
            return False
        
        try:
            self.lib = self.zlibrary.AsyncZlib()
            
            if email and password:
                await self.lib.login(email, password)
                print("✅ Authenticated")
            else:
                print("ℹ️ No authentication")
            
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    async def batch_search(self, search_list: List[Dict]):
        """Process multiple searches"""
        print(f"🔄 Processing {len(search_list)} searches...")
        
        all_results = {}
        
        for i, search_config in enumerate(search_list, 1):
            query = search_config.get('query', '')
            count = search_config.get('count', 10)
            
            print(f"\n[{i}/{len(search_list)}] Searching: '{query}'")
            
            try:
                paginator = await self.lib.search(q=query, count=count)
                results = await paginator.next()
                
                all_results[query] = {
                    'config': search_config,
                    'results': results,
                    'count': len(results),
                    'timestamp': datetime.now().isoformat()
                }
                
                print(f"✅ Found {len(results)} books for '{query}'")
                
                # Small delay between searches
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Failed '{query}': {e}")
                all_results[query] = {
                    'config': search_config,
                    'results': [],
                    'count': 0,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
        
        return all_results
    
    def save_batch_results(self, all_results: Dict, batch_name: str = "batch"):
        """Save batch results in multiple formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{batch_name}_{timestamp}"
        
        # Save JSON
        json_file = self.results_dir / "json" / f"{base_filename}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"💾 JSON saved: {json_file}")
        
        # Save CSV summary
        csv_file = self.results_dir / "csv" / f"{base_filename}_summary.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Query', 'Results Count', 'Status', 'Timestamp'])
            
            for query, data in all_results.items():
                status = 'Success' if data['count'] > 0 else 'No Results'
                if 'error' in data:
                    status = 'Error'
                
                writer.writerow([
                    query,
                    data['count'],
                    status,
                    data['timestamp']
                ])
        
        print(f"📊 CSV summary: {csv_file}")
        
        # Save detailed CSV with all books
        detailed_csv = self.results_dir / "csv" / f"{base_filename}_detailed.csv"
        with open(detailed_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Search Query', 'Book Title', 'Authors', 'Year', 
                'Format', 'Size', 'Rating', 'Publisher', 'URL'
            ])
            
            for query, data in all_results.items():
                for book in data['results']:
                    authors = ", ".join([a.get('author', '') for a in book.get('authors', [])])
                    
                    writer.writerow([
                        query,
                        book.get('name', ''),
                        authors,
                        book.get('year', ''),
                        book.get('extension', ''),
                        book.get('size', ''),
                        book.get('rating', ''),
                        book.get('publisher', ''),
                        book.get('url', '')
                    ])
        
        print(f"📋 Detailed CSV: {detailed_csv}")
        
        return json_file, csv_file, detailed_csv
    
    def generate_report(self, all_results: Dict, batch_name: str = "batch"):
        """Generate detailed text report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.results_dir / "reports" / f"{batch_name}_report_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Z-Library Batch Search Report\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Batch Name: {batch_name}\n")
            f.write(f"Total Searches: {len(all_results)}\n\n")
            
            # Summary statistics
            total_books = sum(data['count'] for data in all_results.values())
            successful_searches = sum(1 for data in all_results.values() if data['count'] > 0)
            failed_searches = sum(1 for data in all_results.values() if 'error' in data)
            
            f.write("SUMMARY STATISTICS\n")
            f.write("-" * 30 + "\n")
            f.write(f"Total books found: {total_books}\n")
            f.write(f"Successful searches: {successful_searches}\n")
            f.write(f"Failed searches: {failed_searches}\n")
            f.write(f"No results: {len(all_results) - successful_searches - failed_searches}\n\n")
            
            # Detailed results
            f.write("DETAILED RESULTS\n")
            f.write("-" * 30 + "\n")
            
            for query, data in all_results.items():
                f.write(f"\nSearch: '{query}'\n")
                f.write(f"Count: {data['count']} books\n")
                f.write(f"Time: {data['timestamp']}\n")
                
                if 'error' in data:
                    f.write(f"Error: {data['error']}\n")
                elif data['results']:
                    f.write("Top results:\n")
                    for i, book in enumerate(data['results'][:3], 1):
                        authors = ", ".join([a.get('author', 'Unknown') for a in book.get('authors', [])])
                        f.write(f"  {i}. {book.get('name', 'Unknown')}\n")
                        f.write(f"     Author: {authors}\n")
                        f.write(f"     Year: {book.get('year', 'Unknown')}\n")
                        f.write(f"     Format: {book.get('extension', 'Unknown')}\n")
                else:
                    f.write("No results found\n")
                
                f.write("\n")
        
        print(f"📄 Report generated: {report_file}")
        return report_file


def create_sample_batch():
    """Create sample batch configuration"""
    return [
        {'query': 'python programming', 'count': 10},
        {'query': 'machine learning', 'count': 8},
        {'query': 'data science', 'count': 8},
        {'query': 'web development', 'count': 6},
        {'query': 'artificial intelligence', 'count': 6},
        {'query': 'cybersecurity', 'count': 5},
        {'query': 'cloud computing', 'count': 5},
        {'query': 'mobile development', 'count': 4},
        {'query': 'database design', 'count': 4},
        {'query': 'software architecture', 'count': 4}
    ]

async def run_sample_batch():
    """Run sample batch processing"""
    print("🔄 Sample Batch Processing")
    print("=" * 40)
    
    bot = BatchZBot()
    
    if not await bot.connect():
        print("❌ Cannot connect")
        return
    
    # Create sample batch
    batch_config = create_sample_batch()
    
    print(f"📋 Batch configuration:")
    for item in batch_config:
        print(f"   - '{item['query']}' ({item['count']} results)")
    
    # Process batch
    results = await bot.batch_search(batch_config)
    
    # Save results
    json_file, csv_file, detailed_csv = bot.save_batch_results(results, "sample_tech_books")
    
    # Generate report
    report_file = bot.generate_report(results, "sample_tech_books")
    
    # Summary
    total_books = sum(data['count'] for data in results.values())
    successful = sum(1 for data in results.values() if data['count'] > 0)
    
    print(f"\n✅ Batch completed!")
    print(f"📚 Total books: {total_books}")
    print(f"✅ Successful: {successful}/{len(batch_config)}")
    print(f"📁 Files in: {bot.results_dir}")

async def custom_batch():
    """Run custom batch from user input"""
    print("🎯 Custom Batch Processing")
    print("=" * 40)
    
    bot = BatchZBot()
    
    if not await bot.connect():
        print("❌ Cannot connect")
        return
    
    # Get batch configuration from user
    batch_config = []
    batch_name = input("Batch name (optional): ").strip() or "custom_batch"
    
    print("\nEnter search queries (empty line to finish):")
    while True:
        query = input("Query: ").strip()
        if not query:
            break
        
        try:
            count = int(input("Count (default 10): ").strip() or 10)
        except ValueError:
            count = 10
        
        batch_config.append({'query': query, 'count': count})
        print(f"✅ Added: '{query}' ({count} results)")
    
    if not batch_config:
        print("❌ No queries entered")
        return
    
    # Process batch
    print(f"\n🔄 Processing {len(batch_config)} searches...")
    results = await bot.batch_search(batch_config)
    
    # Save and report
    bot.save_batch_results(results, batch_name)
    bot.generate_report(results, batch_name)
    
    total_books = sum(data['count'] for data in results.values())
    print(f"\n✅ Custom batch '{batch_name}' completed!")
    print(f"📚 Total books found: {total_books}")

def main():
    """Main function"""
    print("📦 Batch Z-Library Bot")
    print("Individual batch processing tool")
    print("\nChoose mode:")
    print("1. Run sample batch (tech books)")
    print("2. Create custom batch")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        asyncio.run(run_sample_batch())
    elif choice == "2":
        asyncio.run(custom_batch())
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()