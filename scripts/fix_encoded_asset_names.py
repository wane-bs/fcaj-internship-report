import os
import re
import urllib.parse

BASE_DIR = r"d:\DebianBackup\source_code\fcaj\aws-doc"

fixed_files = 0
renamed_assets = 0

for root, dirs, files in os.walk(BASE_DIR):
    # Process assets folders to rename any file with % in its name
    if os.path.basename(root) == "assets" or "assets" in root:
        for f in files:
            if "%" in f:
                decoded = urllib.parse.unquote(f)
                # Replace apostrophe or quote with clean dash/underscore to be safe on Windows/VS Code
                clean_name = decoded.replace("'", "_prime_").replace('"', '_')
                clean_name = re.sub(r'%[0-9a-fA-F]{2}', '', clean_name)
                old_path = os.path.join(root, f)
                new_path = os.path.join(root, clean_name)
                try:
                    os.rename(old_path, new_path)
                    print(f"[RENAME ASSET] {f} -> {clean_name}")
                    renamed_assets += 1
                except Exception as e:
                    print(f"[ERROR RENAME] {f}: {e}")

# Now update all markdown references in aws-doc
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith(".md"):
            fp = os.path.join(root, f)
            with open(fp, "r", encoding="utf-8", errors="ignore") as stream:
                content = stream.read()
            
            # Check if there are %27 or % in image links
            def fix_img_link(match):
                alt = match.group(1)
                link = match.group(2)
                if "%" in link:
                    decoded = urllib.parse.unquote(link)
                    clean_link = decoded.replace("'", "_prime_").replace('"', '_')
                    clean_link = re.sub(r'%[0-9a-fA-F]{2}', '', clean_link)
                    return f"![{alt}]({clean_link})"
                return match.group(0)

            new_content = re.sub(r'!\[(.*?)\]\((assets/[^)]+)\)', fix_img_link, content)
            if new_content != content:
                with open(fp, "w", encoding="utf-8") as stream:
                    stream.write(new_content)
                print(f"[FIXED MD] {f}")
                fixed_files += 1

print(f"\nDone! Renamed {renamed_assets} asset files and updated {fixed_files} markdown files.")
