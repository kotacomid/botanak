#!/usr/bin/env python3
"""
Book Scraping Bot - Main Entry Point
A comprehensive bot for scraping books from Anna's Archive & LibGen
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import List, Optional
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from config.settings import settings, validate_config
from core import BookScraper, MetadataProcessor, FileDownloader, BookMetadata

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rich console for beautiful output
console = Console()


class BookScrapingBot:
    """Main bot class that orchestrates all operations"""
    
    def __init__(self):
        self.scraper = BookScraper()
        self.downloader = FileDownloader()
        self.metadata_processor = MetadataProcessor()
        
        # Validate configuration
        warnings = validate_config()
        if warnings:
            console.print("[yellow]Configuration warnings:[/yellow]")
            for warning in warnings:
                console.print(f"  ⚠️  {warning}")
            console.print()
    
    def search_and_process(self, query: str, limit: int = 10, download: bool = True) -> List[BookMetadata]:
        """Search for books and process them"""
        console.print(f"🔍 Searching for: [bold]{query}[/bold]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Search phase
            search_task = progress.add_task("Searching sources...", total=None)
            results = self.scraper.search_all_sources(query, limit)
            progress.remove_task(search_task)
            
            if not results:
                console.print("[red]❌ No books found[/red]")
                return []
            
            console.print(f"✅ Found {len(results)} books")
            
            # Download phase
            if download and (settings.DOWNLOAD_BOOKS or settings.DOWNLOAD_COVERS):
                download_task = progress.add_task("Downloading files...", total=len(results))
                
                for i, metadata in enumerate(results):
                    # Download book file
                    if settings.DOWNLOAD_BOOKS and metadata.download_url:
                        book_path = self.downloader.download_book(metadata)
                        if book_path:
                            metadata.local_file_path = book_path
                    
                    # Download cover
                    if settings.DOWNLOAD_COVERS and metadata.cover_url:
                        cover_path = self.downloader.download_cover(metadata)
                        if cover_path:
                            metadata.local_cover_path = cover_path
                    
                    progress.advance(download_task)
                
                progress.remove_task(download_task)
            
            # Save metadata
            save_task = progress.add_task("Saving metadata...", total=None)
            self._save_results(results)
            progress.remove_task(save_task)
        
        return results
    
    def _save_results(self, results: List[BookMetadata]):
        """Save results in various formats"""
        if not results:
            return
        
        # Save individual JSON files
        if settings.SAVE_METADATA_JSON:
            for metadata in results:
                self.metadata_processor.save_metadata_json(metadata)
        
        # Save combined CSV
        if settings.SAVE_METADATA_CSV:
            self.metadata_processor.save_metadata_csv(results)
        
        console.print("💾 Metadata saved")
    
    def display_results(self, results: List[BookMetadata]):
        """Display results in a nice table"""
        if not results:
            return
        
        table = Table(title="📚 Search Results")
        table.add_column("Title", style="cyan", no_wrap=False, max_width=30)
        table.add_column("Author", style="magenta", max_width=20)
        table.add_column("Year", justify="center", style="green", width=6)
        table.add_column("Format", justify="center", style="blue", width=8)
        table.add_column("Size", justify="center", style="yellow", width=10)
        table.add_column("Source", style="red", width=12)
        table.add_column("Status", justify="center", width=10)
        
        for metadata in results:
            # Determine status
            status_icons = []
            if metadata.local_file_path:
                status_icons.append("📄")
            if metadata.local_cover_path:
                status_icons.append("🖼️")
            status = "".join(status_icons) or "❌"
            
            table.add_row(
                metadata.title[:30] + "..." if len(metadata.title) > 30 else metadata.title,
                metadata.author[:20] + "..." if len(metadata.author) > 20 else metadata.author,
                str(metadata.year) if metadata.year else "N/A",
                metadata.file_format or "N/A",
                metadata.file_size or "N/A",
                metadata.source,
                status
            )
        
        console.print(table)
    
    def get_stats(self) -> dict:
        """Get bot statistics"""
        download_stats = self.downloader.get_download_stats()
        enabled_features = settings.get_enabled_features()
        
        return {
            'downloads': download_stats,
            'features': enabled_features,
            'tier': 'Premium' if settings.IS_PREMIUM else 'Free'
        }
    
    def close(self):
        """Cleanup resources"""
        self.scraper.close()
        self.downloader.close()


# CLI Commands
@click.group()
@click.option('--debug', is_flag=True, help='Enable debug mode')
def cli(debug):
    """Book Scraping Bot - Scrape books from Anna's Archive & LibGen"""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)


@cli.command()
@click.argument('query')
@click.option('--limit', '-l', default=10, help='Number of results per source')
@click.option('--no-download', is_flag=True, help='Skip downloading files')
@click.option('--source', type=click.Choice(['annas-archive', 'libgen']), help='Specific source to search')
def search(query, limit, no_download, source):
    """Search for books by title or author"""
    bot = BookScrapingBot()
    
    try:
        if source:
            results = bot.scraper.search_book(query, source=source)
        else:
            results = bot.search_and_process(query, limit, download=not no_download)
        
        bot.display_results(results)
        
        # Show summary
        if results:
            console.print(f"\n✅ Found {len(results)} books")
            if not no_download:
                stats = bot.get_stats()
                console.print(f"📥 Downloaded {stats['downloads']['books_downloaded']} books")
                console.print(f"🖼️ Downloaded {stats['downloads']['covers_downloaded']} covers")
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        if settings.DEBUG:
            raise
    finally:
        bot.close()


@cli.command()
@click.argument('title')
@click.option('--author', '-a', help='Author name')
@click.option('--source', type=click.Choice(['annas-archive', 'libgen']), help='Specific source')
def book(title, author, source):
    """Search for a specific book by title and author"""
    bot = BookScrapingBot()
    
    try:
        results = bot.scraper.search_book(title, author or "", source)
        bot.display_results(results)
        
        if results:
            console.print(f"\n✅ Found {len(results)} results for '{title}'")
    
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        if settings.DEBUG:
            raise
    finally:
        bot.close()


@cli.command()
def stats():
    """Show bot statistics and configuration"""
    bot = BookScrapingBot()
    
    try:
        stats = bot.get_stats()
        
        # Create info panel
        info_text = f"""
[bold]Tier:[/bold] {stats['tier']}
[bold]Version:[/bold] {settings.VERSION}
[bold]Output Directory:[/bold] {settings.OUTPUT_DIR}
        """
        
        console.print(Panel(info_text.strip(), title="📊 Bot Information"))
        
        # Download statistics
        downloads = stats['downloads']
        download_table = Table(title="📥 Download Statistics")
        download_table.add_column("Metric", style="cyan")
        download_table.add_column("Value", style="green")
        
        download_table.add_row("Books Downloaded", str(downloads['books_downloaded']))
        download_table.add_row("Covers Downloaded", str(downloads['covers_downloaded']))
        download_table.add_row("Total Book Size", f"{downloads['total_book_size_mb']:.1f} MB")
        download_table.add_row("Total Cover Size", f"{downloads['total_cover_size_mb']:.1f} MB")
        
        console.print(download_table)
        
        # Enabled features
        features = stats['features']
        feature_table = Table(title="🔧 Enabled Features")
        feature_table.add_column("Feature", style="cyan")
        feature_table.add_column("Status", style="green")
        
        for feature, enabled in features.items():
            status = "✅ Enabled" if enabled else "❌ Disabled"
            feature_table.add_row(feature.replace('_', ' ').title(), status)
        
        console.print(feature_table)
    
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
    finally:
        bot.close()


@cli.command()
def config():
    """Show current configuration"""
    console.print(Panel("⚙️ Configuration", style="blue"))
    
    config_table = Table()
    config_table.add_column("Setting", style="cyan")
    config_table.add_column("Value", style="green")
    
    # Key settings
    key_settings = [
        ("IS_PREMIUM", settings.IS_PREMIUM),
        ("DOWNLOAD_BOOKS", settings.DOWNLOAD_BOOKS),
        ("DOWNLOAD_COVERS", settings.DOWNLOAD_COVERS),
        ("GDRIVE_ENABLED", settings.GDRIVE_ENABLED),
        ("FTP_ENABLED", settings.FTP_ENABLED),
        ("MAX_FILE_SIZE_MB", settings.MAX_FILE_SIZE_MB),
        ("SCRAPING_DELAY", settings.SCRAPING_DELAY),
    ]
    
    for setting, value in key_settings:
        config_table.add_row(setting, str(value))
    
    console.print(config_table)
    
    # Show warnings
    warnings = validate_config()
    if warnings:
        console.print("\n[yellow]⚠️ Configuration Warnings:[/yellow]")
        for warning in warnings:
            console.print(f"  • {warning}")


@cli.command()
def cleanup():
    """Clean up incomplete downloads and temporary files"""
    bot = BookScrapingBot()
    
    try:
        console.print("🧹 Cleaning up files...")
        bot.downloader.cleanup_failed_downloads()
        console.print("✅ Cleanup completed")
    
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
    finally:
        bot.close()


def main():
    """Main entry point"""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye! 👋[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]❌ Fatal error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()