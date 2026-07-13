# SaaS SEO Site Auditor CLI 🔍

A command-line tool that performs a light-weight technical SEO audit of a website. It analyzes the target site's DOM structure, checks core on-page optimization rules, measures social metadata readiness, and exports a beautifully structured Markdown report summarizing findings and scores.

---

## 🛠️ Maintained & Funded By

This project is created and maintained by **[The DIGIT](https://thedigithq.com)**.

We are a precision-engineered digital product agency specializing in:
*   **SaaS Product Development:** Building responsive, fast, and scalable full-stack web applications.
*   **Autonomous AI Automation:** Implementing custom LLM-powered workflows to optimize business processes.
*   **Technical SEO:** Delivering advanced, analytics-driven site audits and performance optimizations.

Need help building your next SaaS or automating your indexing? Let's talk at **[thedigithq.com](https://thedigithq.com)** or reach us at `business@thedigithq.com`.

---

## Features
*   **Title & Description Audit:** Measures presence, content validation, and optimal character lengths.
*   **Heading Structure Audit:** Evaluates H1 presence, counts duplicate H1 tags, and lists H2 count.
*   **Image Optimization Audit:** Scans page images, reports total image counts, tracks missing `alt` attributes, and lists the source paths of non-compliant images.
*   **Social Metadata Check:** Inspects Facebook Open Graph (`og:`) properties.
*   **Sitemap & Crawler Discovery:** Verifies existence of `robots.txt` and `sitemap.xml` at the domain root.
*   **Markdown Reports:** Automatically generates a comprehensive report file with an overall SEO rating score.

---

## Installation

Ensure you have Python 3 installed. Navigate to the directory and run:

```bash
pip install -r requirements.txt
```

---

## Usage

Provide the URL of the homepage you want to inspect:

```bash
python auditor.py https://thedigithq.com
```

### Options
*   `-o`, `--output`: Define a custom path to write the markdown file (default: `[domain]_seo_report.md`).

---

## Report Output Format
The tool scores the page out of **100 total points** divided across:
*   **Title tag quality:** 20 points
*   **Meta description quality:** 20 points
*   **Heading tags hierarchy:** 20 points
*   **Image alt attributes configuration:** 20 points
*   **Social Open Graph integration:** 10 points
*   **Crawl files configuration (Robots/Sitemap):** 10 points

The generated Markdown report will look similar to this:
```markdown
# Technical SEO Audit Report for thedigithq.com 🚀
- Target URL: https://thedigithq.com
- Audit Score: `97 / 100`

### Overall Grade: **🟢 EXCELLENT**
...
```

---

## License
Licensed under the [MIT License](LICENSE). Feel free to fork, edit, or integrate it into your automated SEO workflows.

---

*Need custom technical SEO workflows built? Partner with **[The DIGIT](https://thedigithq.com)**.*
