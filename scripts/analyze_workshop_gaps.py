import os
import re
from urllib.parse import urlparse

BASE_DIR = r"d:\DebianBackup\source_code\fcaj\aws-doc"

# Collect all sources currently in aws-doc
existing_hosts = set()
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith(".md"):
            fp = os.path.join(root, f)
            try:
                with open(fp, "r", encoding="utf-8", errors="ignore") as stream:
                    for _ in range(15):
                        line = stream.readline()
                        m = re.match(r"^source:\s*(https?://[^\s]+)", line)
                        if m:
                            host = urlparse(m.group(1)).netloc
                            existing_hosts.add(host)
                            break
            except:
                pass

print(f"Existing Workshop Hosts in aws-doc ({len(existing_hosts)} hosts):")
for h in sorted(existing_hosts):
    print(f"  - {h}")

# Scan links from 00-cloud-journey-roadmap
roadmap_dir = os.path.join(BASE_DIR, "00-cloud-journey-roadmap")
cloudjourney_links = []
link_pattern = re.compile(r'\[([^\]]+)\]\((https?://([0-9a-zA-Z\.\-]+)/vi/[^)]*)\)')

for root, dirs, files in os.walk(roadmap_dir):
    for f in files:
        if f.endswith(".md"):
            fp = os.path.join(root, f)
            with open(fp, "r", encoding="utf-8", errors="ignore") as stream:
                text = stream.read()
                matches = link_pattern.findall(text)
                for title, url, host in matches:
                    cloudjourney_links.append((title.strip(), url.strip(), host.strip()))

# Deduplicate
unique_workshops = {}
for title, url, host in cloudjourney_links:
    if host not in unique_workshops:
        unique_workshops[host] = (title, url)

print(f"\nTotal Sub-Workshops found in Cloud Journey: {len(unique_workshops)}")

missing_workshops = []
present_workshops = []

for host, (title, url) in sorted(unique_workshops.items()):
    if host in existing_hosts:
        present_workshops.append((host, title, url))
    else:
        missing_workshops.append((host, title, url))

print(f"\nAlready Present ({len(present_workshops)}):")
for h, t, u in present_workshops:
    print(f"  [x] {h} : {t}")

print(f"\nMissing / Needs Download ({len(missing_workshops)}):")
for h, t, u in missing_workshops:
    print(f"  [ ] {h} : {t} ({u})")

# Write report to scratch / artifact
report_path = os.path.join(r"C:\Users\FUJITSU\.gemini\antigravity-ide\brain\19f67f38-9df3-4ddd-bd15-0e53956c0c7e", "workshop_gap_analysis.md")
with open(report_path, "w", encoding="utf-8") as rep:
    rep.write("# Báo Cáo Đối Chiếu Kho Workshop AWS: Cloud Journey vs `aws-doc`\n\n")
    rep.write(f"- **Tổng số workshop trên Cloud Journey**: {len(unique_workshops)}\n")
    rep.write(f"- **Đã có trong `aws-doc`**: {len(present_workshops)}\n")
    rep.write(f"- **Chưa có (cần nạp tiếp)**: {len(missing_workshops)}\n\n")
    rep.write("## Danh Sách Các Workshop Chưa Có (Missing Queue)\n\n")
    rep.write("| Mã Host / Workshop | Tên Workshop | Đường Dẫn Gốc |\n")
    rep.write("| :--- | :--- | :--- |\n")
    for h, t, u in missing_workshops:
        rep.write(f"| `{h}` | {t} | [{u}]({u}) |\n")

print(f"\nReport written to {report_path}")
