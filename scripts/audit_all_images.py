import os
import re

BASE_DIR = r"d:\DebianBackup\source_code\fcaj\aws-doc"

print(f"Scanning for broken image links and encoded image paths in {BASE_DIR}...")

broken_report = []
total_md = 0
total_img = 0

for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith(".md"):
            total_md += 1
            md_path = os.path.join(root, f)
            with open(md_path, "r", encoding="utf-8", errors="ignore") as stream:
                content = stream.read()
            
            matches = re.finditer(r'!\[.*?\]\(([^)]+)\)', content)
            for m in matches:
                total_img += 1
                img_path = m.group(1).strip()
                if not img_path.startswith("http://") and not img_path.startswith("https://"):
                    # Check relative file existence
                    full_img_path = os.path.normpath(os.path.join(root, img_path))
                    if not os.path.exists(full_img_path):
                        broken_report.append({
                            'md_file': os.path.relpath(md_path, BASE_DIR),
                            'img_ref': img_path,
                            'resolved_path': full_img_path
                        })

print(f"Scanned {total_md} Markdown files, {total_img} image tags found.")
print(f"Total broken / unresolvable image links: {len(broken_report)}")

for item in broken_report[:30]:
    print(f"  [BROKEN] in {item['md_file']}: {item['img_ref']}")

if len(broken_report) > 30:
    print(f"  ... and {len(broken_report) - 30} more.")
