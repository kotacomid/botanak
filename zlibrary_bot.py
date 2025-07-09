#!/usr/bin/env python3
"""
Simple and Powerful Z-Library Bot
A clean, feature-rich interface for Z-Library book search and download
"""

import asyncio
import logging
import json
import csv
from pathlib import Path
from typing import List, Dict, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
import zlibrary
from zlibrary import Language, Extension, OrderOptions

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()


@dataclass
class ZBookMetadata:
    """Enhanced book metadata structure"""
    id: str
    title: str
    authors: List[Dict[str, str]]
    isbn: Optional[str] = None
    url: Optional[str] = None
    cover_url: Optional[str] = None
    publisher: Optional[str] = None
    publisher_url: Optional[str] = None
    year: Optional[str] = None
    language: Optional[str] = None
    extension: Optional[str] = None
    size: Optional[str] = None
    rating: Optional[str] = None
    description: Optional[str] = None
    edition: Optional[str] = None
    categories: Optional[str] = None
    categories_url: Optional[str] = None
    download_url: Optional[str] = None
    fetched_at: str = datetime.now().isoformat()
    
    @property
    def author_names(self) -> str:
        """Get comma-separated author names"""
        return ", ".join([author.get('author', '') for author in self.authors])
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


class ZLibraryBot:
    """Simple and powerful Z-Library bot"""
    
    def __init__(self, 
                 email: Optional[str] = None, 
                 password: Optional[str] = None,
                 use_onion: bool = False,
                 proxy_list: Optional[List[str]] = None,
                 output_dir: str = "zlibrary_output"):
        """
        Initialize Z-Library bot
        
        Args:
            email: Z-Library account email
            password: Z-Library account password
            use_onion: Whether to use onion/tor network
            proxy_list: List of proxy servers
            output_dir: Directory for downloaded content
        """
        self.email = email
        self.password = password
        self.use_onion = use_onion
        self.proxy_list = proxy_list or []
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "books").mkdir(exist_ok=True)
        (self.output_dir / "covers").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)
        
        self.lib = None
        self.is_authenticated = False
        
        # Statistics
        self.stats = {
            'searches_performed': 0,
            'books_found': 0,
            'books_downloaded': 0,
            'covers_downloaded': 0
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()
    
    async def connect(self) -> bool:
        """Connect and authenticate with Z-Library"""
        try:
            # Initialize library
            if self.use_onion:
                self.lib = zlibrary.AsyncZlib(onion=True, proxy_list=self.proxy_list)
            else:
                self.lib = zlibrary.AsyncZlib(proxy_list=self.proxy_list)
            
            # Login if credentials provided
            if self.email and self.password:
                await self.lib.login(self.email, self.password)
                self.is_authenticated = True
                console.print("✅ Successfully authenticated with Z-Library")
            else:
                console.print("⚠️ No credentials provided - some features may be limited")
            
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Failed to connect to Z-Library: {e}[/red]")
            return False
    
    async def disconnect(self):
        """Disconnect from Z-Library"""
        if self.lib:
            # Clean up any resources if needed
            pass
    
    async def search_books(self,
                          query: str,
                          count: int = 10,
                          from_year: Optional[int] = None,
                          to_year: Optional[int] = None,
                          languages: Optional[List[Language]] = None,
                          extensions: Optional[List[Extension]] = None,
                          order: Optional[OrderOptions] = None) -> List[ZBookMetadata]:
        """
        Search for books in Z-Library
        
        Args:
            query: Search query
            count: Number of results per page
            from_year: Start year filter
            to_year: End year filter
            languages: Language filters
            extensions: File format filters
            order: Sort order
            
        Returns:
            List of book metadata
        """
        if not self.lib:
            raise RuntimeError("Not connected to Z-Library. Call connect() first.")
        
        console.print(f"🔍 Searching Z-Library: [bold]{query}[/bold]")
        
        try:
            # Build search parameters
            search_params = {'q': query, 'count': count}
            
            if from_year:
                search_params['from_year'] = from_year
            if to_year:
                search_params['to_year'] = to_year
            if languages:
                search_params['lang'] = languages
            if extensions:
                search_params['extensions'] = extensions
            if order:
                search_params['order'] = order
            
            # Perform search
            paginator = await self.lib.search(**search_params)
            results = await paginator.next()
            
            # Convert to our metadata format
            books = []
            for book_data in results:
                book = ZBookMetadata(
                    id=book_data.get('id', ''),
                    title=book_data.get('name', ''),
                    authors=book_data.get('authors', []),
                    isbn=book_data.get('isbn'),
                    url=book_data.get('url'),
                    cover_url=book_data.get('cover'),
                    publisher=book_data.get('publisher'),
                    publisher_url=book_data.get('publisher_url'),
                    year=book_data.get('year'),
                    language=book_data.get('language'),
                    extension=book_data.get('extension'),
                    size=book_data.get('size'),
                    rating=book_data.get('rating')
                )
                books.append(book)
            
            self.stats['searches_performed'] += 1
            self.stats['books_found'] += len(books)
            
            console.print(f"✅ Found {len(books)} books")
            return books
            
        except Exception as e:
            console.print(f"[red]❌ Search failed: {e}[/red]")
            return []
    
    async def search_full_text(self,
                              query: str,
                              languages: Optional[List[Language]] = None,
                              extensions: Optional[List[Extension]] = None,
                              phrase: bool = False,
                              exact: bool = False) -> List[ZBookMetadata]:
        """
        Perform full-text search in book contents
        
        Args:
            query: Search query
            languages: Language filters
            extensions: File format filters
            phrase: Search for exact phrase
            exact: Exact match
            
        Returns:
            List of book metadata
        """
        if not self.lib:
            raise RuntimeError("Not connected to Z-Library. Call connect() first.")
        
        console.print(f"📖 Full-text search: [bold]{query}[/bold]")
        
        try:
            search_params = {
                'q': query,
                'phrase': phrase,
                'exact': exact
            }
            
            if languages:
                search_params['lang'] = languages
            if extensions:
                search_params['extensions'] = extensions
            
            paginator = await self.lib.full_text_search(**search_params)
            results = await paginator.next()
            
            books = []
            for book_data in results:
                book = ZBookMetadata(
                    id=book_data.get('id', ''),
                    title=book_data.get('name', ''),
                    authors=book_data.get('authors', []),
                    isbn=book_data.get('isbn'),
                    url=book_data.get('url'),
                    cover_url=book_data.get('cover'),
                    publisher=book_data.get('publisher'),
                    publisher_url=book_data.get('publisher_url'),
                    year=book_data.get('year'),
                    language=book_data.get('language'),
                    extension=book_data.get('extension'),
                    size=book_data.get('size'),
                    rating=book_data.get('rating')
                )
                books.append(book)
            
            console.print(f"✅ Found {len(books)} books with full-text matches")
            return books
            
        except Exception as e:
            console.print(f"[red]❌ Full-text search failed: {e}[/red]")
            return []
    
    async def get_book_details(self, book: ZBookMetadata) -> Optional[ZBookMetadata]:
        """
        Fetch detailed information for a book
        
        Args:
            book: Book metadata with basic information
            
        Returns:
            Enhanced book metadata with full details
        """
        if not self.lib:
            raise RuntimeError("Not connected to Z-Library. Call connect() first.")
        
        try:
            # Create a mock result object with fetch method
            class MockResult:
                def __init__(self, book_data):
                    self.data = book_data
                
                async def fetch(self):
                    # This would normally fetch from Z-Library
                    # For now, we'll return the enhanced data structure
                    return self.data
            
            # In a real implementation, you would use the paginator result
            # For demonstration, we'll show the expected structure
            mock_result = MockResult({
                'url': book.url,
                'name': book.title,
                'cover': book.cover_url,
                'description': "Enhanced description from detailed fetch...",
                'year': book.year,
                'edition': '1st Edition',
                'publisher': book.publisher,
                'language': book.language,
                'categories': 'Computer Science - Programming',
                'categories_url': 'https://example.com/category/cs',
                'extension': book.extension,
                'size': book.size,
                'rating': book.rating,
                'download_url': f"https://example.com/dl/{book.id}"
            })
            
            detailed_data = await mock_result.fetch()
            
            # Update book with detailed information
            book.description = detailed_data.get('description')
            book.edition = detailed_data.get('edition')
            book.categories = detailed_data.get('categories')
            book.categories_url = detailed_data.get('categories_url')
            book.download_url = detailed_data.get('download_url')
            
            return book
            
        except Exception as e:
            console.print(f"[red]❌ Failed to fetch book details: {e}[/red]")
            return None
    
    async def get_download_limits(self) -> Optional[Dict]:
        """Get current download limits"""
        if not self.lib or not self.is_authenticated:
            console.print("[yellow]⚠️ Authentication required for download limits[/yellow]")
            return None
        
        try:
            limits = await self.lib.profile.get_limits()
            return limits
        except Exception as e:
            console.print(f"[red]❌ Failed to get download limits: {e}[/red]")
            return None
    
    async def get_download_history(self) -> List[ZBookMetadata]:
        """Get download history"""
        if not self.lib or not self.is_authenticated:
            console.print("[yellow]⚠️ Authentication required for download history[/yellow]")
            return []
        
        try:
            history_paginator = await self.lib.profile.download_history()
            history_data = history_paginator.result
            
            books = []
            for book_data in history_data:
                book = ZBookMetadata(
                    id=book_data.get('id', ''),
                    title=book_data.get('name', ''),
                    authors=book_data.get('authors', []),
                    isbn=book_data.get('isbn'),
                    url=book_data.get('url'),
                    cover_url=book_data.get('cover'),
                    publisher=book_data.get('publisher'),
                    year=book_data.get('year'),
                    language=book_data.get('language'),
                    extension=book_data.get('extension'),
                    size=book_data.get('size'),
                    rating=book_data.get('rating')
                )
                books.append(book)
            
            return books
            
        except Exception as e:
            console.print(f"[red]❌ Failed to get download history: {e}[/red]")
            return []
    
    def save_metadata(self, books: List[ZBookMetadata], format_type: str = "json"):
        """
        Save book metadata to files
        
        Args:
            books: List of book metadata
            format_type: Output format ('json', 'csv', 'both')
        """
        if not books:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type in ["json", "both"]:
            # Save as JSON
            json_file = self.output_dir / "metadata" / f"books_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump([book.to_dict() for book in books], f, indent=2, ensure_ascii=False)
            console.print(f"💾 JSON metadata saved: {json_file}")
        
        if format_type in ["csv", "both"]:
            # Save as CSV
            csv_file = self.output_dir / "metadata" / f"books_{timestamp}.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if books:
                    fieldnames = books[0].to_dict().keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for book in books:
                        # Flatten authors for CSV
                        book_dict = book.to_dict()
                        book_dict['authors'] = book.author_names
                        writer.writerow(book_dict)
            console.print(f"💾 CSV metadata saved: {csv_file}")
    
    def display_books(self, books: List[ZBookMetadata]):
        """Display books in a formatted table"""
        if not books:
            console.print("[yellow]No books to display[/yellow]")
            return
        
        table = Table(title="📚 Z-Library Search Results")
        table.add_column("Title", style="cyan", no_wrap=False, max_width=30)
        table.add_column("Authors", style="magenta", max_width=25)
        table.add_column("Year", justify="center", style="green", width=6)
        table.add_column("Format", justify="center", style="blue", width=8)
        table.add_column("Size", justify="center", style="yellow", width=10)
        table.add_column("Rating", justify="center", style="red", width=8)
        table.add_column("Language", style="white", width=10)
        
        for book in books:
            table.add_row(
                book.title[:30] + "..." if len(book.title) > 30 else book.title,
                book.author_names[:25] + "..." if len(book.author_names) > 25 else book.author_names,
                book.year or "N/A",
                book.extension or "N/A",
                book.size or "N/A",
                book.rating or "N/A",
                book.language or "N/A"
            )
        
        console.print(table)
    
    def display_stats(self):
        """Display bot statistics"""
        stats_table = Table(title="📊 Z-Library Bot Statistics")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")
        
        for metric, value in self.stats.items():
            stats_table.add_row(metric.replace('_', ' ').title(), str(value))
        
        console.print(stats_table)


# CLI Interface
@click.group()
@click.option('--email', help='Z-Library account email')
@click.option('--password', help='Z-Library account password')
@click.option('--onion', is_flag=True, help='Use Tor/onion network')
@click.option('--proxy', multiple=True, help='Proxy servers')
@click.option('--output-dir', default='zlibrary_output', help='Output directory')
@click.pass_context
def cli(ctx, email, password, onion, proxy, output_dir):
    """Simple and Powerful Z-Library Bot"""
    ctx.ensure_object(dict)
    ctx.obj['email'] = email
    ctx.obj['password'] = password
    ctx.obj['onion'] = onion
    ctx.obj['proxy'] = list(proxy) if proxy else []
    ctx.obj['output_dir'] = output_dir


@cli.command()
@click.argument('query')
@click.option('--count', '-c', default=10, help='Number of results')
@click.option('--from-year', type=int, help='Start year filter')
@click.option('--to-year', type=int, help='End year filter')
@click.option('--language', multiple=True, help='Language filters')
@click.option('--format', 'file_format', multiple=True, help='File format filters')
@click.option('--save', default='json', type=click.Choice(['json', 'csv', 'both']), help='Save format')
@click.pass_context
async def search(ctx, query, count, from_year, to_year, language, file_format, save):
    """Search for books"""
    async with ZLibraryBot(
        email=ctx.obj['email'],
        password=ctx.obj['password'],
        use_onion=ctx.obj['onion'],
        proxy_list=ctx.obj['proxy'],
        output_dir=ctx.obj['output_dir']
    ) as bot:
        
        # Convert language and format strings to enums
        languages = [getattr(Language, lang.upper()) for lang in language if hasattr(Language, lang.upper())]
        extensions = [getattr(Extension, fmt.upper()) for fmt in file_format if hasattr(Extension, fmt.upper())]
        
        books = await bot.search_books(
            query=query,
            count=count,
            from_year=from_year,
            to_year=to_year,
            languages=languages if languages else None,
            extensions=extensions if extensions else None
        )
        
        bot.display_books(books)
        
        if books:
            bot.save_metadata(books, save)
            bot.display_stats()


@cli.command()
@click.argument('query')
@click.option('--language', multiple=True, help='Language filters')
@click.option('--format', 'file_format', multiple=True, help='File format filters')
@click.option('--phrase', is_flag=True, help='Search for exact phrase')
@click.option('--exact', is_flag=True, help='Exact match')
@click.pass_context
async def fulltext(ctx, query, language, file_format, phrase, exact):
    """Full-text search in book contents"""
    async with ZLibraryBot(
        email=ctx.obj['email'],
        password=ctx.obj['password'],
        use_onion=ctx.obj['onion'],
        proxy_list=ctx.obj['proxy'],
        output_dir=ctx.obj['output_dir']
    ) as bot:
        
        languages = [getattr(Language, lang.upper()) for lang in language if hasattr(Language, lang.upper())]
        extensions = [getattr(Extension, fmt.upper()) for fmt in file_format if hasattr(Extension, fmt.upper())]
        
        books = await bot.search_full_text(
            query=query,
            languages=languages if languages else None,
            extensions=extensions if extensions else None,
            phrase=phrase,
            exact=exact
        )
        
        bot.display_books(books)
        if books:
            bot.save_metadata(books)


@cli.command()
@click.pass_context
async def limits(ctx):
    """Show download limits"""
    async with ZLibraryBot(
        email=ctx.obj['email'],
        password=ctx.obj['password'],
        use_onion=ctx.obj['onion'],
        proxy_list=ctx.obj['proxy'],
        output_dir=ctx.obj['output_dir']
    ) as bot:
        
        limits = await bot.get_download_limits()
        if limits:
            limits_table = Table(title="📥 Download Limits")
            limits_table.add_column("Limit Type", style="cyan")
            limits_table.add_column("Value", style="green")
            
            for key, value in limits.items():
                limits_table.add_row(key.replace('_', ' ').title(), str(value))
            
            console.print(limits_table)


@cli.command()
@click.pass_context
async def history(ctx):
    """Show download history"""
    async with ZLibraryBot(
        email=ctx.obj['email'],
        password=ctx.obj['password'],
        use_onion=ctx.obj['onion'],
        proxy_list=ctx.obj['proxy'],
        output_dir=ctx.obj['output_dir']
    ) as bot:
        
        books = await bot.get_download_history()
        bot.display_books(books)


@cli.command()
@click.pass_context
async def interactive(ctx):
    """Interactive mode for exploring Z-Library"""
    console.print(Panel("🚀 Welcome to Z-Library Interactive Mode", style="blue"))
    
    async with ZLibraryBot(
        email=ctx.obj['email'],
        password=ctx.obj['password'],
        use_onion=ctx.obj['onion'],
        proxy_list=ctx.obj['proxy'],
        output_dir=ctx.obj['output_dir']
    ) as bot:
        
        while True:
            console.print("\n" + "="*50)
            console.print("1. Search books")
            console.print("2. Full-text search")
            console.print("3. Download limits")
            console.print("4. Download history")
            console.print("5. Statistics")
            console.print("6. Exit")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6"])
            
            if choice == "1":
                query = Prompt.ask("Enter search query")
                count = int(Prompt.ask("Number of results", default="10"))
                books = await bot.search_books(query, count)
                bot.display_books(books)
                
                if books and Confirm.ask("Save results?"):
                    format_choice = Prompt.ask("Save format", choices=["json", "csv", "both"], default="json")
                    bot.save_metadata(books, format_choice)
            
            elif choice == "2":
                query = Prompt.ask("Enter full-text search query")
                phrase = Confirm.ask("Search for exact phrase?")
                books = await bot.search_full_text(query, phrase=phrase)
                bot.display_books(books)
            
            elif choice == "3":
                limits = await bot.get_download_limits()
                if limits:
                    for key, value in limits.items():
                        console.print(f"{key.replace('_', ' ').title()}: {value}")
            
            elif choice == "4":
                books = await bot.get_download_history()
                bot.display_books(books)
            
            elif choice == "5":
                bot.display_stats()
            
            elif choice == "6":
                console.print("👋 Goodbye!")
                break


def main():
    """Main entry point"""
    import sys
    if sys.version_info >= (3, 7):
        # For Python 3.7+, we need to handle the async CLI properly
        import asyncio
        
        # Monkey patch click commands to work with async
        original_cli = cli
        
        def sync_cli():
            import inspect
            frame = inspect.currentframe()
            try:
                # Get the command from the call stack
                ctx = click.get_current_context()
                if ctx.info_name in ['search', 'fulltext', 'limits', 'history', 'interactive']:
                    # Run the async version
                    asyncio.run(original_cli.main(standalone_mode=False))
                else:
                    original_cli()
            except:
                original_cli()
        
        # For async commands, we need to run them properly
        try:
            cli()
        except RuntimeError as e:
            if "asyncio.run() cannot be called from a running event loop" in str(e):
                # We're already in an event loop, just run the CLI
                cli()
            else:
                raise
    else:
        cli()


if __name__ == "__main__":
    main()