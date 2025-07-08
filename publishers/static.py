"""
Static HTML Generator
Creates beautiful static HTML pages for books
"""

import os
from pathlib import Path
from typing import List, Dict
from jinja2 import Environment, FileSystemLoader, Template
import logging

from config.settings import settings
from core.metadata import BookMetadata

logger = logging.getLogger(__name__)


class StaticHTMLGenerator:
    """Generate static HTML pages for books"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir or settings.OUTPUT_DIR)
        self.html_dir = self.output_dir / "html"
        self.html_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup Jinja2 environment
        template_dir = Path("templates")
        if template_dir.exists():
            self.env = Environment(loader=FileSystemLoader(str(template_dir)))
        else:
            # Fallback to basic templates
            self.env = Environment(loader=FileSystemLoader('.'))
            logger.warning("Templates directory not found, using fallback")
    
    def generate_book_page(self, metadata: BookMetadata) -> str:
        """Generate individual book page"""
        try:
            # Load template
            template = self.env.get_template('book_page.html')
            
            # Render HTML
            html_content = template.render(book=metadata)
            
            # Save to file
            filename = f"{metadata.filename_base}.html"
            filepath = self.html_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Generated book page: {filename}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error generating book page for {metadata.title}: {e}")
            return self._generate_fallback_page(metadata)
    
    def generate_book_list_page(self, books: List[BookMetadata], 
                              title: str = "Book Library", 
                              query: str = "") -> str:
        """Generate book listing page"""
        try:
            # Load template
            template = self.env.get_template('book_list.html')
            
            # Prepare data
            stats = {
                'total_books': len(books),
                'sources': list(set(book.source for book in books if book.source))
            }
            
            # Render HTML
            html_content = template.render(
                books=books,
                query=query,
                title=title,
                stats=stats
            )
            
            # Save to file
            filename = f"book_list_{query.replace(' ', '_') if query else 'all'}.html"
            filepath = self.html_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Generated book list page: {filename}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error generating book list page: {e}")
            return self._generate_fallback_list_page(books, title)
    
    def generate_index_page(self, featured_books: List[BookMetadata]) -> str:
        """Generate main index page"""
        try:
            # Use book list template for index
            return self.generate_book_list_page(
                featured_books, 
                title="Featured Books - Free Download Library"
            )
            
        except Exception as e:
            logger.error(f"Error generating index page: {e}")
            return ""
    
    def generate_sitemap(self, books: List[BookMetadata]) -> str:
        """Generate XML sitemap"""
        try:
            sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
            
            # Add index page
            sitemap_content += '''  <url>
    <loc>/</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
'''
            
            # Add individual book pages
            for book in books:
                sitemap_content += f'''  <url>
    <loc>/book/{book.filename_base}.html</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
'''
            
            sitemap_content += '</urlset>'
            
            # Save sitemap
            sitemap_path = self.html_dir / "sitemap.xml"
            with open(sitemap_path, 'w', encoding='utf-8') as f:
                f.write(sitemap_content)
            
            logger.info("Generated sitemap.xml")
            return str(sitemap_path)
            
        except Exception as e:
            logger.error(f"Error generating sitemap: {e}")
            return ""
    
    def generate_rss_feed(self, books: List[BookMetadata], 
                         title: str = "Latest Books", 
                         description: str = "Latest free books") -> str:
        """Generate RSS feed"""
        try:
            from datetime import datetime
            
            rss_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{title}</title>
    <description>{description}</description>
    <language>en-us</language>
    <lastBuildDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")}</lastBuildDate>
'''
            
            # Add recent books
            for book in books[:20]:  # Latest 20 books
                pub_date = book.scraped_at.strftime("%a, %d %b %Y %H:%M:%S %z") if book.scraped_at else ""
                
                rss_content += f'''
    <item>
      <title>{self._escape_xml(book.title)}</title>
      <description>by {self._escape_xml(book.author)} - {self._escape_xml(book.description[:200] if book.description else '')}</description>
      <link>/book/{book.filename_base}.html</link>
      <guid>/book/{book.filename_base}.html</guid>
      <pubDate>{pub_date}</pubDate>
    </item>'''
            
            rss_content += '''
  </channel>
</rss>'''
            
            # Save RSS feed
            rss_path = self.html_dir / "feed.xml"
            with open(rss_path, 'w', encoding='utf-8') as f:
                f.write(rss_content)
            
            logger.info("Generated RSS feed")
            return str(rss_path)
            
        except Exception as e:
            logger.error(f"Error generating RSS feed: {e}")
            return ""
    
    def _escape_xml(self, text: str) -> str:
        """Escape XML special characters"""
        if not text:
            return ""
        
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#39;'))
    
    def _generate_fallback_page(self, metadata: BookMetadata) -> str:
        """Generate basic HTML page without template"""
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>{metadata.title} by {metadata.author}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .book {{ max-width: 800px; margin: 0 auto; }}
        .title {{ color: #333; font-size: 2rem; margin-bottom: 10px; }}
        .author {{ color: #666; font-size: 1.2rem; margin-bottom: 20px; }}
        .meta {{ background: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .download {{ background: #007cba; color: white; padding: 15px 30px; 
                     text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }}
        .download:hover {{ background: #005a8b; }}
    </style>
</head>
<body>
    <div class="book">
        <h1 class="title">{metadata.title}</h1>
        <div class="author">by {metadata.author}</div>
        
        <div class="meta">
            <strong>Format:</strong> {metadata.file_format}<br>
            <strong>Size:</strong> {metadata.file_size}<br>
            <strong>Source:</strong> {metadata.source}<br>
            {f'<strong>Year:</strong> {metadata.year}<br>' if metadata.year else ''}
            {f'<strong>ISBN:</strong> {metadata.isbn}<br>' if metadata.isbn else ''}
        </div>
        
        {f'<p><strong>Description:</strong><br>{metadata.description}</p>' if metadata.description else ''}
        
        {f'<a href="{metadata.download_url}" class="download">Download {metadata.file_format or "Book"}</a>' if metadata.download_url else ''}
    </div>
</body>
</html>'''
        
        filename = f"{metadata.filename_base}_fallback.html"
        filepath = self.html_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def _generate_fallback_list_page(self, books: List[BookMetadata], title: str) -> str:
        """Generate basic book list page without template"""
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .books {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .book {{ border: 1px solid #ddd; padding: 20px; border-radius: 5px; }}
        .book-title {{ font-size: 1.2rem; font-weight: bold; margin-bottom: 10px; }}
        .book-author {{ color: #666; margin-bottom: 10px; }}
        .book-meta {{ font-size: 0.9rem; color: #888; }}
        .download {{ background: #007cba; color: white; padding: 10px 20px; 
                     text-decoration: none; border-radius: 3px; display: inline-block; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <p>Found {len(books)} books</p>
        
        <div class="books">
'''
        
        for book in books:
            html_content += f'''
            <div class="book">
                <div class="book-title">{book.title}</div>
                <div class="book-author">by {book.author}</div>
                <div class="book-meta">
                    {book.file_format} • {book.file_size} • {book.source}
                </div>
                {f'<a href="{book.download_url}" class="download">Download</a>' if book.download_url else ''}
            </div>'''
        
        html_content += '''
        </div>
    </div>
</body>
</html>'''
        
        filename = f"{title.replace(' ', '_').lower()}_fallback.html"
        filepath = self.html_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def generate_all_pages(self, books: List[BookMetadata]) -> Dict[str, str]:
        """Generate all pages for a list of books"""
        results = {}
        
        # Generate individual book pages
        for book in books:
            try:
                page_path = self.generate_book_page(book)
                results[f"book_{book.filename_base}"] = page_path
            except Exception as e:
                logger.error(f"Error generating page for {book.title}: {e}")
        
        # Generate list pages
        try:
            results["index"] = self.generate_index_page(books)
            results["all_books"] = self.generate_book_list_page(books)
            results["sitemap"] = self.generate_sitemap(books)
            results["rss"] = self.generate_rss_feed(books)
        except Exception as e:
            logger.error(f"Error generating list pages: {e}")
        
        logger.info(f"Generated {len(results)} HTML files")
        return results