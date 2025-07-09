#!/usr/bin/env python3
"""
Batch Z-Library Bot
Process multiple searches and generate reports
"""

import asyncio
import json
import csv
from pathlib import Path
from datetime import datetime

def check_zlibrary():
    """Check zlibrary"""
    try:
        import zlibrary
        print("✅ zlibrary available")
        return True, zlibrary
    except ImportError:
        print("❌ zlibrary not available")
        return False, None

class BatchZBot:
    """Batch processing Z-Library bot"""
    
    def __init__(self):
        """Initialize batch bot"""
        self.available, self.zlibrary = check_zlibrary()
        self.lib = None
        self.results_dir = Path("batch_results")
        self.results_dir.mkdir(exist_ok=True)
        
        # Create subdirs
        (self.results_dir / "json").mkdir(exist_ok=True)
        (self.results_dir / "csv").mkdir(exist_ok=True)
        (self.results_dir / "reports").mkdir(exist_ok=True)
        
        if self.available:
            print(f"📁 Results: {self.results_dir}")
    
    async def connect(self):
        """Connect to Z-Library"""
        if not self.available:
            return False
        
        try:
            self.lib = self.zlibrary.AsyncZlib()
            print("✅ Connected")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    async def batch_search(self, queries):
        """Process multiple searches"""
        print(f"🔄 Processing {len(queries)} searches...")
        
        results = {}
        
        for i, config in enumerate(queries, 1):
            query = config['query']
            count = config.get('count', 10)
            
            print(f"[{i}/{len(queries)}] {query}")
            
            try:
                paginator = await self.lib.search(q=query, count=count)
                search_results = await paginator.next()
                
                results[query] = {
                    'results': search_results,
                    'count': len(search_results),
                    'timestamp': datetime.now().isoformat()
                }
                
                print(f"✅ {len(search_results)} books")
                await asyncio.sleep(0.3)  # Rate limit
                
            except Exception as e:
                print(f"❌ Failed: {e}")
                results[query] = {
                    'results': [],
                    'count': 0,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
        
        return results
    
    def save_results(self, results, name="batch"):
        """Save in multiple formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = f"{name}_{timestamp}"
        
        # JSON
        json_file = self.results_dir / "json" / f"{base}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"💾 JSON: {json_file}")
        
        # CSV Summary
        csv_file = self.results_dir / "csv" / f"{base}_summary.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Query', 'Count', 'Status'])
            
            for query, data in results.items():
                status = 'Success' if data['count'] > 0 else 'No Results'
                if 'error' in data:
                    status = 'Error'
                writer.writerow([query, data['count'], status])
        
        print(f"📊 CSV: {csv_file}")
        
        # Report
        report_file = self.results_dir / "reports" / f"{base}_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"Batch Report: {name}\n")
            f.write("=" * 40 + "\n")
            f.write(f"Generated: {datetime.now()}\n\n")
            
            total = sum(data['count'] for data in results.values())
            f.write(f"Total searches: {len(results)}\n")
            f.write(f"Total books: {total}\n\n")
            
            for query, data in results.items():
                f.write(f"Query: {query}\n")
                f.write(f"Results: {data['count']}\n")
                if 'error' in data:
                    f.write(f"Error: {data['error']}\n")
                f.write("\n")
        
        print(f"📄 Report: {report_file}")
        return json_file, csv_file, report_file


def sample_queries():
    """Sample tech queries"""
    return [
        {'query': 'python programming', 'count': 8},
        {'query': 'machine learning', 'count': 6},
        {'query': 'web development', 'count': 6},
        {'query': 'data science', 'count': 5},
        {'query': 'artificial intelligence', 'count': 5},
    ]

async def run_sample():
    """Run sample batch"""
    print("🔄 Sample Tech Books Batch")
    print("=" * 30)
    
    bot = BatchZBot()
    
    if not await bot.connect():
        return
    
    queries = sample_queries()
    print("Queries:")
    for q in queries:
        print(f"  - {q['query']} ({q['count']} results)")
    
    results = await bot.batch_search(queries)
    bot.save_results(results, "tech_books")
    
    total = sum(data['count'] for data in results.values())
    successful = sum(1 for data in results.values() if data['count'] > 0)
    
    print(f"\n✅ Batch completed!")
    print(f"📚 Total books: {total}")
    print(f"✅ Successful: {successful}/{len(queries)}")

async def custom_batch():
    """Custom batch"""
    print("🎯 Custom Batch")
    print("=" * 20)
    
    bot = BatchZBot()
    
    if not await bot.connect():
        return
    
    queries = []
    name = input("Batch name: ").strip() or "custom"
    
    print("Enter queries (empty to finish):")
    while True:
        query = input("Query: ").strip()
        if not query:
            break
        
        try:
            count = int(input("Count (10): ").strip() or 10)
        except ValueError:
            count = 10
        
        queries.append({'query': query, 'count': count})
        print(f"✅ Added: {query}")
    
    if not queries:
        print("No queries entered")
        return
    
    results = await bot.batch_search(queries)
    bot.save_results(results, name)
    
    total = sum(data['count'] for data in results.values())
    print(f"\n✅ Custom batch completed!")
    print(f"📚 Total books: {total}")

def main():
    """Main"""
    print("📦 Batch Z-Library Bot")
    print("1. Sample tech books")
    print("2. Custom batch")
    
    choice = input("Choose (1/2): ").strip()
    
    if choice == "1":
        asyncio.run(run_sample())
    elif choice == "2":
        asyncio.run(custom_batch())
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()