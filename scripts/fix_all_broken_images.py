import os
import re

BASE_DIR = r"d:\DebianBackup\source_code\fcaj\aws-doc"

# 1. Clean up broken .html image references in markdown files
cleaned_html_tags = 0
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith(".md"):
            fp = os.path.join(root, f)
            with open(fp, "r", encoding="utf-8", errors="ignore") as stream:
                content = stream.read()
            
            # Remove ![alt](...html) or ![alt](...htm)
            new_content = re.sub(r'!\[.*?\]\([^)]+\.html?\)', '', content)
            if new_content != content:
                with open(fp, "w", encoding="utf-8") as stream:
                    stream.write(new_content)
                cleaned_html_tags += 1
                print(f"[CLEANED HTML IMG TAGS] in {f}")

print(f"Cleaned broken HTML image tags in {cleaned_html_tags} files.")

# 2. Build global catalog of all asset files and folders
assets_catalog = {} # filename -> list of absolute paths
folder_catalog = {} # folder_name -> list of absolute paths

for root, dirs, files in os.walk(BASE_DIR):
    dname = os.path.basename(root)
    if dname not in folder_catalog:
        folder_catalog[dname] = []
    folder_catalog[dname].append(root)
    
    for f in files:
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp')):
            if f not in assets_catalog:
                assets_catalog[f] = []
            assets_catalog[f].append(os.path.join(root, f))

# 3. Scan and fix remaining broken image references
fixed_refs = 0
still_broken = 0

for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith(".md"):
            md_path = os.path.join(root, f)
            with open(md_path, "r", encoding="utf-8", errors="ignore") as stream:
                content = stream.read()
            
            def fix_img(match):
                global fixed_refs, still_broken
                alt = match.group(1)
                img_ref = match.group(2).strip()
                if img_ref.startswith("http://") or img_ref.startswith("https://"):
                    return match.group(0)
                
                full_path = os.path.normpath(os.path.join(root, img_ref))
                if os.path.exists(full_path):
                    return match.group(0)
                
                # Try finding by basename
                base_img = os.path.basename(img_ref)
                if base_img in assets_catalog:
                    candidates = assets_catalog[base_img]
                    # Pick candidate in the same module first
                    current_module = os.path.relpath(root, BASE_DIR).split(os.sep)[0]
                    best = None
                    for c in candidates:
                        if current_module in c:
                            best = c
                            break
                    if not best:
                        best = candidates[0]
                    
                    rel = os.path.relpath(best, root).replace("\\", "/")
                    fixed_refs += 1
                    print(f"  [FIXED] in {f}: {img_ref} -> {rel}")
                    return f"![{alt}]({rel})"
                
                # Check if entire subfolder exists in another module
                parts = img_ref.split("/")
                if len(parts) > 1:
                    subf = parts[0]
                    if subf in folder_catalog:
                        best_f = folder_catalog[subf][0]
                        candidate_img = os.path.join(best_f, parts[1])
                        if os.path.exists(candidate_img):
                            rel = os.path.relpath(candidate_img, root).replace("\\", "/")
                            fixed_refs += 1
                            print(f"  [FIXED VIA FOLDER] in {f}: {img_ref} -> {rel}")
                            return f"![{alt}]({rel})"
                
                still_broken += 1
                return match.group(0)

            new_content = re.sub(r'!\[(.*?)\]\(([^)]+)\)', fix_img, content)
            if new_content != content:
                with open(md_path, "w", encoding="utf-8") as stream:
                    stream.write(new_content)

print(f"\nFinal Summary: Fixed {fixed_refs} broken image references.")
print(f"Remaining broken references: {still_broken}")
