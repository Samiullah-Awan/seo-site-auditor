# Building a CLI SEO Auditor with Python and BeautifulSoup

When launching a new web application or managing a content-heavy SaaS site, auditing on-page SEO factors is a routine but vital task. Missing alt tags, duplicate H1 tags, or poorly formatted meta descriptions can drag down search rankings, hurting organic user acquisition.

While tools like Screaming Frog or Ahrefs are excellent, they are either paid, heavy, or run in closed ecosystems. 

As a web developer, building your own lightweight SEO auditor is surprisingly straightforward. In this tutorial, we will write a Python command-line tool using `BeautifulSoup` and `requests` to analyze any web page, check it against standard on-page SEO metrics, and export a structured Markdown report.

---

## Technical Architecture
Our tool will perform the following steps:
1. **Fetch the target page:** Send an HTTP request with a standard browser User-Agent to avoid scraping blocks.
2. **Parse the DOM:** Extract HTML elements (title, description, headings, images, and Open Graph tags).
3. **Audit against rules:** Grade each element (presence, length, structure, alt tags ratio).
4. **Generate a score:** Calculate an SEO score out of 100 points.
5. **Export reports:** Write the results as a Markdown file.

---

## Step 1: Setting Up the Workspace

Create a new directory and install the required libraries:
```bash
pip install requests beautifulsoup4
```

* `requests` will download the page.
* `beautifulsoup4` will allow us to navigate the HTML structure like a DOM tree.

---

## Step 2: Requesting the Page
Some servers block standard script requests (like the default user agent of the `requests` library) to prevent scraping. We bypass this by mimicking a standard Chrome browser:

```python
import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')
```

---

## Step 3: Implementing the SEO Audit Logic

We will evaluate six key areas:
1. **Title Tag:** Length should ideally be between 50-60 characters.
2. **Meta Description:** Length should be between 120-160 characters.
3. **H1 Heading:** There must be exactly one H1 tag on the page.
4. **Image Alt Tags:** All image tags must have an `alt` description.
5. **Open Graph Metadata:** Verify if social sharing properties (`og:title`, `og:description`, `og:image`) are present.
6. **Crawl Files:** Check if `robots.txt` and `sitemap.xml` are accessible.

### 1. Auditing Titles and Descriptions
Here is how to extract and evaluate these elements:

```python
def audit_title(soup):
    title_tag = soup.find('title')
    if not title_tag or not title_tag.text.strip():
        return {"value": "", "score": 0, "status": "missing"}
        
    title_text = title_tag.text.strip()
    length = len(title_text)
    
    if 50 <= length <= 60:
        return {"value": title_text, "score": 20, "status": "optimal"}
    elif length < 30 or length > 60:
        return {"value": title_text, "score": 10, "status": "suboptimal"}
    else:
        return {"value": title_text, "score": 15, "status": "acceptable"}
```

### 2. Headings and Image Alt Attributes
A clean heading hierarchy is essential for search crawlers. Multiple H1 tags confuse crawler bots regarding the main theme of the page.

```python
def audit_headings(soup):
    h1s = soup.find_all('h1')
    h1_count = len(h1s)
    
    score = 0
    if h1_count == 1:
        score = 20
    elif h1_count > 1:
        score = 10 # Deduct points for duplicate headers
        
    return {"h1_count": h1_count, "score": score}

def audit_images(soup):
    images = soup.find_all('img')
    if not images:
        return {"total": 0, "missing_alt": 0, "score": 20}
        
    missing_alt = sum(1 for img in images if not img.get('alt') or not img.get('alt').strip())
    alt_ratio = (len(images) - missing_alt) / len(images)
    
    return {
        "total": len(images),
        "missing_alt": missing_alt,
        "score": int(alt_ratio * 20)
    }
```

---

## Step 4: Generating the Markdown Report
A console printout is useful, but generating a shareable report file makes the CLI tool practical for client deliveries.

```python
def write_markdown_report(domain, score, audit_data):
    report = []
    report.append(f"# Technical SEO Audit Report for {domain}")
    report.append(f"- **Overall Score:** `{score} / 100`")
    
    # Render sections
    report.append("## 1. Title Tag Status")
    report.append(f"- Title: `{audit_data['title']['value']}`")
    report.append(f"- Status: {audit_data['title']['status'].upper()}")
    
    report.append("## 2. Image Optimization")
    report.append(f"- Total Images: {audit_data['images']['total']}")
    report.append(f"- Missing Alt Tags: {audit_data['images']['missing_alt']}")
    
    with open(f"{domain}_seo_report.md", "w") as f:
        f.write("\n".join(report))
```

---

## Running Your SEO Auditor

By joining these modules, you can build a powerful scanner. Running the auditor against a live site is simple:

```bash
python auditor.py https://thedigithq.com
```

The output will automatically generate a localized `thedigithq.com_seo_report.md` report highlighting exact fixes to boost page authority.

---

## Get the Source Code

If you want to view a fully realized version of this tool, check out the repository maintained by **[The DIGIT](https://thedigithq.com)** on GitHub:
👉 **[Samiullah-Awan/seo-site-auditor](https://github.com/Samiullah-Awan/seo-site-auditor)**

The repository includes:
- Deep checks for Facebook Open Graph and Twitter Card tags.
- Programmatic crawling checks verifying root `robots.txt` and `sitemap.xml` presence.
- Pre-configured color grading and report exporting format.

---

## Building Authority for Your Website

This auditor focuses on basic on-page configurations. But building massive search presence requires an experienced strategy: fast load times, semantic rendering layouts, backlink building campaigns, and programmatic site maps.

If you are scaling a SaaS or need automated systems implemented for your business, let's collaborate. 

Learn more at **[The DIGIT](https://thedigithq.com)** or reach out to our team at **[business@thedigithq.com](mailto:business@thedigithq.com)**.
