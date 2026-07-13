#!/usr/bin/env python3
import os
import sys
import argparse
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

def parse_args():
    parser = argparse.ArgumentParser(
        description="SaaS SEO Site Auditor CLI - Powered by The DIGIT (thedigithq.com)"
    )
    parser.add_argument(
        "url",
        help="The target website URL to audit (e.g., https://thedigithq.com)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to save the Markdown report (default: [domain]_seo_report.md)"
    )
    return parser.parse_args()

def verify_url(url):
    """Ensure URL is absolute and starts with http/https"""
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        print("[!] Invalid URL. Please provide an absolute URL (e.g., https://example.com)")
        sys.exit(1)
    return url

def check_robots_and_sitemap(base_url):
    """Checks if robots.txt and sitemap.xml exist at the domain root"""
    results = {
        "robots_txt": {"status": False, "url": ""},
        "sitemap_xml": {"status": False, "url": ""}
    }
    
    parsed = urlparse(base_url)
    root_url = f"{parsed.scheme}://{parsed.netloc}"
    
    robots_url = urljoin(root_url, "/robots.txt")
    sitemap_url = urljoin(root_url, "/sitemap.xml")
    
    try:
        r = requests.get(robots_url, timeout=10)
        if r.status_code == 200:
            results["robots_txt"] = {"status": True, "url": robots_url}
    except requests.RequestException:
        pass
        
    try:
        r = requests.get(sitemap_url, timeout=10)
        if r.status_code == 200:
            results["sitemap_xml"] = {"status": True, "url": sitemap_url}
    except requests.RequestException:
        pass
        
    return results

def run_audit(url):
    print(f"[*] Starting SEO Audit for: {url}")
    
    # 1. Fetch page HTML
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[!] Failed to fetch the website: {e}", file=sys.stderr)
        sys.exit(1)
        
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Initialize audit storage
    audit = {
        "url": url,
        "status_code": response.status_code,
        "title": {"value": "", "status": "missing", "length": 0, "score": 0},
        "description": {"value": "", "status": "missing", "length": 0, "score": 0},
        "headings": {"h1_count": 0, "h1s": [], "h2_count": 0, "score": 0},
        "images": {"total": 0, "missing_alt": 0, "missing_urls": [], "score": 0},
        "open_graph": {"og_title": False, "og_desc": False, "og_image": False, "score": 0},
        "technical": {"robots": False, "sitemap": False, "score": 0},
        "total_score": 0
    }
    
    # 2. Audit Title Tag (Max Score: 20)
    title_tag = soup.find('title')
    if title_tag and title_tag.text.strip():
        title_text = title_tag.text.strip()
        length = len(title_text)
        audit["title"]["value"] = title_text
        audit["title"]["length"] = length
        
        if 50 <= length <= 60:
            audit["title"]["status"] = "optimal"
            audit["title"]["score"] = 20
        elif length < 30:
            audit["title"]["status"] = "too_short"
            audit["title"]["score"] = 10
        elif length > 60:
            audit["title"]["status"] = "too_long"
            audit["title"]["score"] = 12
        else:
            audit["title"]["status"] = "acceptable"
            audit["title"]["score"] = 17
            
    # 3. Audit Meta Description (Max Score: 20)
    desc_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
    if desc_tag and desc_tag.get('content', '').strip():
        desc_text = desc_tag.get('content', '').strip()
        length = len(desc_text)
        audit["description"]["value"] = desc_text
        audit["description"]["length"] = length
        
        if 120 <= length <= 160:
            audit["description"]["status"] = "optimal"
            audit["description"]["score"] = 20
        elif length < 80:
            audit["description"]["status"] = "too_short"
            audit["description"]["score"] = 10
        elif length > 160:
            audit["description"]["status"] = "too_long"
            audit["description"]["score"] = 12
        else:
            audit["description"]["status"] = "acceptable"
            audit["description"]["score"] = 17

    # 4. Audit Headings Structure (Max Score: 20)
    h1s = soup.find_all('h1')
    audit["headings"]["h1_count"] = len(h1s)
    audit["headings"]["h1s"] = [h.text.strip() for h in h1s if h.text.strip()]
    audit["headings"]["h2_count"] = len(soup.find_all('h2'))
    
    if len(h1s) == 1:
        audit["headings"]["score"] = 20
    elif len(h1s) > 1:
        audit["headings"]["score"] = 10  # Penalize duplicate H1s
    else:
        audit["headings"]["score"] = 0

    # 5. Audit Image Alt Tags (Max Score: 20)
    images = soup.find_all('img')
    audit["images"]["total"] = len(images)
    
    missing_alt = 0
    missing_urls = []
    for img in images:
        # Check if alt exists and has non-space content
        alt = img.get('alt')
        if alt is None or alt.strip() == '':
            missing_alt += 1
            src = img.get('src', 'Unknown Src')
            missing_urls.append(urljoin(url, src))
            
    audit["images"]["missing_alt"] = missing_alt
    audit["images"]["missing_urls"] = missing_urls[:10]  # Store up to 10 missing alts
    
    if len(images) == 0:
        audit["images"]["score"] = 20  # No images to audit
    else:
        alt_ratio = (len(images) - missing_alt) / len(images)
        audit["images"]["score"] = int(alt_ratio * 20)

    # 6. Audit Open Graph Meta Tags (Max Score: 10)
    og_title = soup.find('meta', attrs={'property': 'og:title'})
    og_desc = soup.find('meta', attrs={'property': 'og:description'})
    og_image = soup.find('meta', attrs={'property': 'og:image'})
    
    if og_title:
        audit["open_graph"]["og_title"] = True
        audit["open_graph"]["score"] += 3
    if og_desc:
        audit["open_graph"]["og_desc"] = True
        audit["open_graph"]["score"] += 3
    if og_image:
        audit["open_graph"]["og_image"] = True
        audit["open_graph"]["score"] += 4

    # 7. Audit Technicals: robots.txt and sitemap.xml (Max Score: 10)
    tech_check = check_robots_and_sitemap(url)
    if tech_check["robots_txt"]["status"]:
        audit["technical"]["robots"] = True
        audit["technical"]["score"] += 5
    if tech_check["sitemap_xml"]["status"]:
        audit["technical"]["sitemap"] = True
        audit["technical"]["score"] += 5

    # Calculate Total Score
    audit["total_score"] = (
        audit["title"]["score"] + 
        audit["description"]["score"] + 
        audit["headings"]["score"] + 
        audit["images"]["score"] + 
        audit["open_graph"]["score"] + 
        audit["technical"]["score"]
    )
    
    return audit

def generate_report(audit, output_path=None):
    parsed = urlparse(audit["url"])
    domain = parsed.netloc.replace('www.', '')
    
    if not output_path:
        output_path = f"{domain}_seo_report.md"
        
    # Build markdown report
    markdown = []
    markdown.append(f"# Technical SEO Audit Report for {domain} 🚀\n")
    markdown.append(f"- **Target URL:** {audit['url']}")
    markdown.append(f"- **HTTP Status Code:** {audit['status_code']}")
    markdown.append(f"- **Audit Score:** `{audit['total_score']} / 100`\n")
    
    # Score classification bar
    if audit['total_score'] >= 85:
        score_grade = "🟢 EXCELLENT"
    elif audit['total_score'] >= 65:
        score_grade = "🟡 NEEDS TWEAKS"
    else:
        score_grade = "🔴 POOR"
        
    markdown.append(f"### Overall Grade: **{score_grade}**\n")
    markdown.append("---")
    
    # Section: Title Tag
    title = audit["title"]
    markdown.append(f"## 1. Title Tag Status (`{title['score']}/20` pts)")
    if title["status"] == "missing":
        markdown.append("⚠️ **Critical Issue:** Title tag is missing or empty.")
    else:
        status_badges = {
            "optimal": "🟢 Optimal Length (50-60 chars)",
            "acceptable": "🟡 Acceptable Length",
            "too_short": "⚠️ Too Short (<30 chars)",
            "too_long": "⚠️ Too Long (>60 chars)"
        }
        markdown.append(f"- **Current Title:** `{title['value']}`")
        markdown.append(f"- **Length:** {title['length']} characters")
        markdown.append(f"- **Evaluation:** {status_badges.get(title['status'])}")
    markdown.append("")
    
    # Section: Description Tag
    desc = audit["description"]
    markdown.append(f"## 2. Meta Description Status (`{desc['score']}/20` pts)")
    if desc["status"] == "missing":
        markdown.append("⚠️ **Critical Issue:** Meta description is missing or empty.")
    else:
        status_badges = {
            "optimal": "🟢 Optimal Length (120-160 chars)",
            "acceptable": "🟡 Acceptable Length",
            "too_short": "⚠️ Too Short (<80 chars)",
            "too_long": "⚠️ Too Long (>160 chars)"
        }
        markdown.append(f"- **Current Meta Description:** `{desc['value']}`")
        markdown.append(f"- **Length:** {desc['length']} characters")
        markdown.append(f"- **Evaluation:** {status_badges.get(desc['status'])}")
    markdown.append("")
    
    # Section: Headings
    headings = audit["headings"]
    markdown.append(f"## 3. Headings Structure (`{headings['score']}/20` pts)")
    markdown.append(f"- **H1 Tags Found:** {headings['h1_count']}")
    if headings["h1_count"] == 1:
        markdown.append(f"  - `H1:` \"{headings['h1s'][0]}\"")
        markdown.append("  - 🟢 **Optimal:** Exactly one H1 tag on the page.")
    elif headings["h1_count"] > 1:
        markdown.append("  - ⚠️ **Issue:** Multiple H1 tags found. It is best practice to have only one main header.")
        for idx, h in enumerate(headings["h1s"], 1):
            markdown.append(f"    {idx}. \"{h}\"")
    else:
        markdown.append("  - 🔴 **Critical:** No H1 tags found on the page.")
    markdown.append(f"- **H2 Tags Found:** {headings['h2_count']}")
    markdown.append("")
    
    # Section: Image Alts
    imgs = audit["images"]
    markdown.append(f"## 4. Image Alternative Attributes (`{imgs['score']}/20` pts)")
    markdown.append(f"- **Total Images Evaluated:** {imgs['total']}")
    markdown.append(f"- **Images Missing Alt Tags:** {imgs['missing_alt']}")
    if imgs["missing_alt"] > 0:
        alt_pct = int(((imgs['total'] - imgs['missing_alt']) / imgs['total']) * 100)
        markdown.append(f"  - ⚠️ **Improvement Area:** Only `{alt_pct}%` of your images contain alt descriptions.")
        markdown.append("  - **Sample URLs missing Alt tags (up to 10):**")
        for url in imgs["missing_urls"]:
            markdown.append(f"    - `{url}`")
    else:
        markdown.append("  - 🟢 **Optimal:** All images contain alt tags.")
    markdown.append("")
    
    # Section: Open Graph
    og = audit["open_graph"]
    markdown.append(f"## 5. Social Open Graph Meta (`{og['score']}/10` pts)")
    markdown.append(f"- **og:title:** {'🟢 Configured' if og['og_title'] else '❌ Missing'}")
    markdown.append(f"- **og:description:** {'🟢 Configured' if og['og_desc'] else '❌ Missing'}")
    markdown.append(f"- **og:image:** {'🟢 Configured' if og['og_image'] else '❌ Missing'}")
    markdown.append("")
    
    # Section: Technical
    tech = audit["technical"]
    markdown.append(f"## 6. Crawler Files (`{tech['score']}/10` pts)")
    markdown.append(f"- **robots.txt:** {'🟢 Found' if tech['robots'] else '⚠️ Missing'}")
    markdown.append(f"- **sitemap.xml:** {'🟢 Found' if tech['sitemap'] else '⚠️ Missing'}")
    markdown.append("\n---")
    
    # Professional Agency footer
    markdown.append("## 🛠️ Need Professional Optimization?")
    markdown.append("This report was compiled utilizing the **SaaS SEO Site Auditor CLI**, powered by **[The DIGIT](https://thedigithq.com)**.")
    markdown.append("We engineer high-performance SaaS platforms, automate operations, and implement technical SEO configurations.")
    markdown.append("Get in touch at **[thedigithq.com](https://thedigithq.com)** or email us at **[business@thedigithq.com](mailto:business@thedigithq.com)** to supercharge your site's SEO, speed, and organic acquisition.")
    
    # Save file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(markdown))
        print(f"[+] Audit complete! Report saved to: {output_path}")
    except Exception as e:
        print(f"[!] Error writing report to file: {e}")
        
    return output_path

def main():
    args = parse_args()
    target_url = verify_url(args.url)
    
    # Run auditing engine
    audit_results = run_audit(target_url)
    
    # Export report
    generate_report(audit_results, args.output)

if __name__ == "__main__":
    main()
