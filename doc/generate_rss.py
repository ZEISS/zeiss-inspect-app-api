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
import html

def extract_feed_items_from_news_md(news_md_file):
    """Extract news items list from the .. feed:: directive in news.md"""
    try:
        content = news_md_file.read_text(encoding='utf-8')
        
        # Find the feed directive section
        feed_match = re.search(r'```\{eval-rst\}\s*\n\.\. feed::(.*?)```', content, re.DOTALL)
        if not feed_match:
            print("No feed directive found in news.md")
            return []
        
        feed_content = feed_match.group(1)
        
        # Extract the list of news items (after the directive parameters)
        lines = feed_content.split('\n')
        items = []
        
        # Skip directive parameters, find news items
        found_items = False
        for line in lines:
            line = line.strip()
            if not line or line.startswith(':'):
                continue
            if not found_items and not re.match(r'\d{8}-', line):
                continue
            found_items = True
            
            # This should be a news item filename (without .md extension)
            if re.match(r'\d{8}-', line):
                items.append(line.strip())
        
        return items
    except Exception as e:
        print(f"Error parsing news.md: {e}")
        return []

def parse_news_file(md_file):
    """Parse a single news markdown file with enhanced description extraction"""
    try:
        content = md_file.read_text(encoding='utf-8')
        
        # Extract date from filename (YYYYMMDD-title.md)
        date_match = re.match(r'(\d{4})(\d{2})(\d{2})-(.*)\.md$', md_file.name)
        if not date_match:
            return None
            
        year, month, day, title_slug = date_match.groups()
        file_date = datetime(int(year), int(month), int(day))
        
        # Try to extract more precise date from feed-entry directive
        feed_entry_date = extract_feed_entry_date(content)
        final_date = feed_entry_date if feed_entry_date else file_date
        
        # Try to extract title from first heading in file
        title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else title_slug.replace('-', ' ').title()
        
        # Extract enhanced description - combine multiple paragraphs but exclude code blocks
        description = extract_description(content)
        
        return {
            'title': title,
            'description': description,
            'date': final_date,
            'link': f"news/{md_file.stem}.html",
            'filename': md_file.stem
        }
    except Exception as e:
        print(f"Error parsing {md_file}: {e}")
        return None

def extract_feed_entry_date(content):
    """Extract date from feed-entry comment if present"""
    try:
        # Look for MyST comment with feed-entry data
        # Format: % feed-entry: date: 2024-12-12 12:00
        feed_entry_match = re.search(r'^%\s*feed-entry:\s*date:\s*(.+?)\s*$', content, re.MULTILINE)
        if feed_entry_match:
            date_str = feed_entry_match.group(1).strip()
            # Parse date string like "2025-01-06 11:00"
            date_formats = [
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d",
                "%Y/%m/%d %H:%M",
                "%Y/%m/%d"
            ]
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
    except Exception:
        pass
    return None

def extract_description(content):
    """Extract a rich description from markdown content"""
    lines = content.split('\n')
    description_lines = []
    in_code_block = False
    found_content = False
    
    for line in lines:
        stripped = line.strip()
        
        # Skip headers
        if stripped.startswith('#'):
            continue
        
        # Skip MyST comments (feed-entry)
        if stripped.startswith('%'):
            continue
            
        # Handle code blocks
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        
        if in_code_block:
            continue
            
        # Skip empty lines at the beginning
        if not stripped and not found_content:
            continue
            
        # If we hit a meaningful line, we've found content
        if stripped:
            found_content = True
            
        # Add line to description
        if found_content:
            description_lines.append(stripped)
            
        # Stop after a reasonable amount of content
        if len(' '.join(description_lines)) > 400:
            break
            
        # Stop at next section (if we hit another header or horizontal rule)
        if stripped.startswith('##') or stripped.startswith('---'):
            break
    
    description = ' '.join(description_lines).strip()
    
    # Clean up markdown syntax for RSS
    description = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', description)  # Remove links but keep text
    description = re.sub(r'\*\*([^*]+)\*\*', r'\1', description)  # Remove bold
    description = re.sub(r'\*([^*]+)\*', r'\1', description)  # Remove italic
    description = re.sub(r'`([^`]+)`', r'\1', description)  # Remove code formatting
    
    # Limit length and add ellipsis if needed
    if len(description) > 500:
        description = description[:497] + "..."
    
    return description or "No description available."

def process_news_md_feed_directive(news_md_file, news_dir):
    """Replace the feed directive in news.md with actual news content"""
    try:
        content = news_md_file.read_text(encoding='utf-8')
        
        # Find the feed directive section
        feed_match = re.search(r'(```\{eval-rst\}\s*\n\.\. feed::.*?```)', content, re.DOTALL)
        if not feed_match:
            print("No feed directive found in news.md")
            return False
        
        feed_block = feed_match.group(1)
        
        # Extract news items from the directive
        news_items = extract_feed_items_from_news_md(news_md_file)
        
        # Generate MyST markdown content for each news item
        news_content_lines = []
        for i, news_item in enumerate(news_items):
            md_file = news_dir / f"{news_item}.md"
            if md_file.exists():
                is_last_item = (i == len(news_items) - 1)
                item_content = generate_news_item_content(md_file, news_item, is_last_item)
                if item_content:
                    news_content_lines.append(item_content)
        
        # Replace the feed directive with the actual content
        replacement_content = "\n\n".join(news_content_lines)
        new_content = content.replace(feed_block, replacement_content)
        
        # Write back to the file
        news_md_file.write_text(new_content, encoding='utf-8')
        print(f"Updated news.md with {len(news_content_lines)} news items")
        return True
        
    except Exception as e:
        print(f"Error processing news.md: {e}")
        return False

def generate_news_item_content(md_file, news_item, is_last_item=False):
    """Generate MyST markdown content for a single news item"""
    try:
        content = md_file.read_text(encoding='utf-8')
        
        # Extract date from feed-entry directive or filename
        feed_entry_date = extract_feed_entry_date(content)
        if not feed_entry_date:
            date_match = re.match(r'(\d{4})(\d{2})(\d{2})-', md_file.name)
            if date_match:
                year, month, day = date_match.groups()
                feed_entry_date = datetime(int(year), int(month), int(day))
        
        # Format date in original format (YYYY-MM-DD HH:MM)
        date_str = feed_entry_date.strftime("%Y-%m-%d %H:%M") if feed_entry_date else "Unknown date"
        
        # Extract title
        title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else news_item.replace('-', ' ').title()
        
        # Generate anchor ID from title (lowercase, replace spaces/special chars with hyphens)
        anchor_id = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower()).replace(' ', '-')
        
        # Create link to individual news file with anchor
        news_file_link = f"{news_item}.html#{anchor_id}"
        
        # Clean content - remove feed-entry directive and first heading
        cleaned_content = clean_content_for_inclusion(content)
        
        # Generate the MyST content with linked heading - omit final separator for last item
        separator = "" if is_last_item else "\n\n---"
        item_html = f"""
<div class="news-item-header">
<h3 class="news-item-title"><a class="feed-ref reference internal" href="{news_file_link}">{title}</a></h3>
<p class="feed-meta">Published on <em class="feed-date">{date_str}</em></p>
</div>

{cleaned_content}{separator}
"""
        return item_html.strip()
        
    except Exception as e:
        print(f"Error generating content for {md_file}: {e}")
        return None

def clean_content_for_inclusion(content):
    """Clean content for inclusion in news.md - remove comments and first heading"""
    lines = content.split('\n')
    cleaned_lines = []
    skip_first_heading = True
    
    for line in lines:
        stripped = line.strip()
        
        # Skip first heading
        if skip_first_heading and stripped.startswith('#'):
            skip_first_heading = False
            continue
            
        # Skip MyST comments (feed-entry)
        if stripped.startswith('%'):
            continue
            
        # Keep the line
        cleaned_lines.append(line)
    
    # Join and clean up extra whitespace
    result = '\n'.join(cleaned_lines).strip()
    
    # Remove excessive blank lines
    result = re.sub(r'\n\n\n+', '\n\n', result)
    
    return result

def generate_rss(items, output_file, base_url):
    """Generate RSS XML from news items with rich descriptions"""
    # Create RSS structure
    rss = ET.Element("rss", version="2.0")
    rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")
    
    channel = ET.SubElement(rss, "channel")
    
    # Channel metadata
    ET.SubElement(channel, "title").text = "ZEISS INSPECT App Python API News"
    ET.SubElement(channel, "description").text = "Latest updates and news for ZEISS INSPECT App development"
    ET.SubElement(channel, "link").text = base_url
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "lastBuildDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # Atom self-reference
    atom_link = ET.SubElement(channel, "atom:link")
    atom_link.set("href", f"{base_url}index.rss")
    atom_link.set("rel", "self")
    atom_link.set("type", "application/rss+xml")
    
    # Add items
    for item_data in items[:10]:  # Limit to 10 most recent items
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = item_data['title']
        
        # Create rich description with HTML escaping
        description = html.escape(item_data['description'])
        ET.SubElement(item, "description").text = description
        
        ET.SubElement(item, "link").text = f"{base_url}{item_data['link']}"
        ET.SubElement(item, "guid").text = f"{base_url}{item_data['link']}"
        ET.SubElement(item, "pubDate").text = item_data['date'].strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # Write XML file
    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ", level=0)  # Pretty print
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Generated RSS feed: {output_file}")

def generate_rss(items, output_file, base_url):
    """Generate RSS XML from news items with rich descriptions"""
    # Create RSS structure
    rss = ET.Element("rss", version="2.0")
    rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")
    
    channel = ET.SubElement(rss, "channel")
    
    # Channel metadata
    ET.SubElement(channel, "title").text = "ZEISS INSPECT App Python API News"
    ET.SubElement(channel, "description").text = "Latest updates and news for ZEISS INSPECT App development"
    ET.SubElement(channel, "link").text = base_url
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "lastBuildDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # Atom self-reference
    atom_link = ET.SubElement(channel, "atom:link")
    atom_link.set("href", f"{base_url}index.rss")
    atom_link.set("rel", "self")
    atom_link.set("type", "application/rss+xml")
    
    # Add items
    for item_data in items[:10]:  # Limit to 10 most recent items
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = item_data['title']
        
        # Create rich description with HTML escaping
        description = html.escape(item_data['description'])
        ET.SubElement(item, "description").text = description
        
        ET.SubElement(item, "link").text = f"{base_url}{item_data['link']}"
        ET.SubElement(item, "guid").text = f"{base_url}{item_data['link']}"
        ET.SubElement(item, "pubDate").text = item_data['date'].strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # Write XML file
    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ", level=0)  # Pretty print
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Generated RSS feed: {output_file}")

def main():
    import sys
    
    # Get paths
    doc_dir = Path(__file__).parent
    build_dir = doc_dir.parent / "_build"
    news_dir = doc_dir / "news"
    news_md_file = news_dir / "news.md"
    
    # Base URL for the site - use environment variable if available (for branch-specific URLs)
    base_url = os.environ.get('GITHUB_PAGES_URL', 'https://zeiss.github.io/zeiss-inspect-app-api/main/')
    if not base_url.endswith('/'):
        base_url += '/'
    
    # FIRST: Extract news items from the feed directive BEFORE modifying the file
    print("Extracting news items list...")
    news_items = extract_feed_items_from_news_md(news_md_file)
    
    if not news_items:
        print("No news items found in news.md feed directive")
        return
    
    print(f"Found {len(news_items)} news items")
    
    # SECOND: Pre-process news.md with feed content
    print("Pre-processing news.md...")
    success = process_news_md_feed_directive(news_md_file, news_dir)
    if not success:
        sys.exit(1)
    print("Pre-processing complete")
    
    # THIRD: Generate RSS feed using the extracted items list
    print("Generating RSS feed...")
    
    # Parse each news file
    items = []
    for news_item in news_items:
        md_file = news_dir / f"{news_item}.md"
        if md_file.exists():
            parsed = parse_news_file(md_file)
            if parsed:
                items.append(parsed)
        else:
            print(f"Warning: News file {md_file} referenced in feed but not found")
    
    if items:
        # Sort by date (most recent first)
        items.sort(key=lambda x: x['date'], reverse=True)
        
        # Generate RSS file in build directory
        rss_file = build_dir / "index.rss"
        build_dir.mkdir(exist_ok=True)
        generate_rss(items, rss_file, base_url)
        print(f"Generated RSS feed with {len(items)} items at {base_url}index.rss")
    else:
        print("No valid news items could be parsed")

if __name__ == "__main__":
    main()