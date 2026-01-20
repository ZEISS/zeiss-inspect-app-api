#!/usr/bin/env python3
"""
Custom RSS feed generator for ZEISS INSPECT App API News
Replaces the unmaintained sphinxcontrib.newsfeed extension
"""

import os
import re
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

def extract_news_items(news_dir):
    """Extract news items from markdown files in the news directory"""
    items = []
    news_path = Path(news_dir)
    
    if not news_path.exists():
        print(f"News directory {news_dir} not found")
        return items
    
    # Find all markdown files that look like news items (YYYYMMDD-*.md)
    for md_file in news_path.glob("*.md"):
        if re.match(r'\d{8}-.*\.md$', md_file.name):
            items.append(parse_news_file(md_file))
    
    # Sort by date (most recent first)
    items.sort(key=lambda x: x['date'], reverse=True)
    return [item for item in items if item]

def parse_news_file(md_file):
    """Parse a single news markdown file"""
    try:
        content = md_file.read_text(encoding='utf-8')
        
        # Extract date from filename (YYYYMMDD-title.md)
        date_match = re.match(r'(\d{4})(\d{2})(\d{2})-(.*)\.md$', md_file.name)
        if not date_match:
            return None
            
        year, month, day, title_slug = date_match.groups()
        
        # Try to extract title from first heading in file
        title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else title_slug.replace('-', ' ').title()
        
        # Extract first paragraph as description
        lines = content.split('\n')
        description = ""
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('```'):
                description = line[:200] + ("..." if len(line) > 200 else "")
                break
        
        return {
            'title': title,
            'description': description,
            'date': datetime(int(year), int(month), int(day)),
            'link': f"news/{md_file.stem}.html",
            'filename': md_file.stem
        }
    except Exception as e:
        print(f"Error parsing {md_file}: {e}")
        return None

def generate_rss(items, output_file, base_url):
    """Generate RSS XML from news items"""
    # Create RSS structure
    rss = ET.Element("rss", version="2.0")
    rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")
    
    channel = ET.SubElement(rss, "channel")
    
    # Channel metadata
    ET.SubElement(channel, "title").text = "ZEISS INSPECT App Python API News"
    ET.SubElement(channel, "description").text = "Latest updates and news for ZEISS INSPECT App development"
    ET.SubElement(channel, "link").text = base_url
    ET.SubElement(channel, "language").text = "en-us"
    
    # Atom self-reference
    atom_link = ET.SubElement(channel, "atom:link")
    atom_link.set("href", f"{base_url}index.rss")
    atom_link.set("rel", "self")
    atom_link.set("type", "application/rss+xml")
    
    # Add items
    for item_data in items[:10]:  # Limit to 10 most recent items
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = item_data['title']
        ET.SubElement(item, "description").text = item_data['description']
        ET.SubElement(item, "link").text = f"{base_url}{item_data['link']}"
        ET.SubElement(item, "guid").text = f"{base_url}{item_data['link']}"
        ET.SubElement(item, "pubDate").text = item_data['date'].strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # Write XML file
    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ", level=0)  # Pretty print
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Generated RSS feed: {output_file}")

def main():
    # Get paths
    doc_dir = Path(__file__).parent
    build_dir = doc_dir.parent / "_build"
    news_dir = doc_dir / "news"
    
    # Base URL for the site
    base_url = "https://zeiss.github.io/zeiss-inspect-app-api/main/"
    
    # Extract news items
    items = extract_news_items(news_dir)
    
    if items:
        # Generate RSS file in build directory
        rss_file = build_dir / "index.rss"
        generate_rss(items, rss_file, base_url)
        print(f"Generated RSS feed with {len(items)} items")
    else:
        print("No news items found")

if __name__ == "__main__":
    main()