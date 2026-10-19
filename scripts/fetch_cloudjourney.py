import urllib.request
import re
import os
from urllib.parse import urljoin, urlparse

BASE_URL = "https://cloudjourney.awsstudygroup.com/vi/"
OUTPUT_DIR = r"d:\DebianBackup\source_code\fcaj\aws-doc\00-cloud-journey-roadmap"
ASSETS_DIR = os.path.join(OUTPUT_DIR, "assets")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def fetch_html(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode('utf-8', errors='ignore')

def download_image(img_url):
    try:
        parsed = urlparse(img_url)
        img_name = os.path.basename(parsed.path)
        if not img_name or '.' not in img_name:
            img_name = "image_" + str(abs(hash(img_url))) + ".png"
        local_path = os.path.join(ASSETS_DIR, img_name)
        if not os.path.exists(local_path):
            req = urllib.request.Request(img_url, headers=HEADERS)
            with urllib.request.urlopen(req) as resp, open(local_path, 'wb') as f:
                f.write(resp.read())
        return f"assets/{img_name}"
    except Exception as e:
        print(f"Error downloading image {img_url}: {e}")
        return img_url

def html_to_markdown(html, page_url):
    # Extract body inner content
    body_match = re.search(r'<div id=body-inner>(.*?)</div>\s*</div>\s*<div id=navigation>', html, re.DOTALL)
    if not body_match:
        body_match = re.search(r'<div id=body-inner>(.*?)</div>', html, re.DOTALL)
    content = body_match.group(1) if body_match else html

    # Extract title
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content)
    title = title_match.group(1).strip() if title_match else "Cloud Journey"

    # Clean up navigation links inside content
    content = re.sub(r'<span id=sidebar-toggle-span>.*?</span>', '', content, flags=re.DOTALL)

    # Process images: <img src="..." alt="...">
    def replace_img(match):
        raw_tag = match.group(0)
        src_match = re.search(r'src=["\']?([^"\' >]+)', raw_tag)
        alt_match = re.search(r'alt=["\']?([^"\' >]*)', raw_tag)
        alt = alt_match.group(1) if alt_match else ""
        if src_match:
            src = src_match.group(1)
            full_src = urljoin(page_url, src)
            local_src = download_image(full_src)
            return f"\n\n![{alt}]({local_src})\n\n"
        return raw_tag

    content = re.sub(r'<img[^>]+>', replace_img, content)

    # Convert headers
    content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n\n', content)
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n\n', content)
    content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n\n', content)
    content = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1\n\n', content)
    content = re.sub(r'<h5[^>]*>(.*?)</h5>', r'##### \1\n\n', content)

    # Convert paragraphs & linebreaks
    content = re.sub(r'<p>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)
    content = re.sub(r'<br\s*/?>', r'\n', content)
    content = re.sub(r'<hr\s*/?>', r'\n---\n\n', content)

    # Convert links <a href="...">text</a>
    def replace_link(match):
        href = match.group(1)
        text = match.group(2)
        full_href = urljoin(page_url, href)
        return f"[{text}]({full_href})"
    content = re.sub(r'<a\s+[^>]*href=["\']?([^"\' >]+)["\']?[^>]*>(.*?)</a>', replace_link, content, flags=re.DOTALL)

    # Convert list items
    content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', content, flags=re.DOTALL)
    content = re.sub(r'</?(?:ul|ol)[^>]*>', r'\n', content)

    # Remove remaining HTML tags
    content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content)
    content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content)
    content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content)
    content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content)
    content = re.sub(r'<[^>]+>', '', content)

    # Unescape HTML entities
    content = content.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    content = re.sub(r'\n{3,}', '\n\n', content).strip()

    frontmatter = f"""---
created: 2026-10-19T11:15:00 (UTC +07:00)
tags: ["Cloud Journey", "AWS Roadmap", "Overview"]
source: {page_url}
author: AWS Study Group
---

# {title}

{content}
"""
    return frontmatter

pages = [
    ("index.md", "https://cloudjourney.awsstudygroup.com/vi/"),
    ("1-explore.md", "https://cloudjourney.awsstudygroup.com/vi/1-explore/"),
    ("2-migrate.md", "https://cloudjourney.awsstudygroup.com/vi/2-migrate/"),
    ("3-optimize.md", "https://cloudjourney.awsstudygroup.com/vi/3-optimize/"),
    ("4-modernize.md", "https://cloudjourney.awsstudygroup.com/vi/4-modernize/"),
    ("5-container.md", "https://cloudjourney.awsstudygroup.com/vi/5-container/"),
    ("6-dataandanalytic.md", "https://cloudjourney.awsstudygroup.com/vi/6-dataandanalytic/"),
    ("7-aimlservice.md", "https://cloudjourney.awsstudygroup.com/vi/7-aimlservice/"),
    ("8-fcjworkforce.md", "https://cloudjourney.awsstudygroup.com/vi/8-fcjworkforce/")
]

for filename, url in pages:
    print(f"Fetching {url} -> {filename}...")
    try:
        html = fetch_html(url)
        md = html_to_markdown(html, url)
        file_path = os.path.join(OUTPUT_DIR, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"  Successfully saved {file_path}")
    except Exception as e:
        print(f"  Failed to fetch {url}: {e}")

print("All Cloud Journey roadmap pages fetched successfully!")
