# How We Built a Suite of Open-Source SEO Tools to Grow Our Agency

Building a digital product agency in a crowded market is a challenge. Direct outbound sales are noisy, and paid advertising (CPC) can quickly drain your resources.

When we founded **[The DIGIT](https://thedigithq.com)**, we decided to take a different approach: **Build in Public & Share Open Source Tools**.

By identifying simple, high-value technical pain points that SaaS founders and developers face daily, we built lightweight open-source utilities. These tools solve immediate problems, showcase our engineering standards, and naturally drive organic traffic back to our agency homepage.

Here is the breakdown of the suite we built and the growth lessons we learned.

---

## 1. Tool 1: GSC Fast Indexer (Python CLI)
* **The Problem:** New startups launch pages, but Google can take weeks to crawl and index them naturally. Manual submission in the Google Search Console UI is slow and limited.
* **Our Solution:** A Python CLI tool that uses Google's Indexing API to submit URLs in bulk. It fetches links from XML sitemaps or text files, authenticates via a Service Account, and notifies Google instantly, reducing crawl latency from weeks to minutes.
* **GitHub Repo:** [gsc-fast-indexer](https://github.com/Samiullah-Awan/gsc-fast-indexer)

---

## 2. Tool 2: React/Next.js SEO Schema Generator
* **The Problem:** Setting up structured data (JSON-LD) for Rich Snippets is tedious, often requiring heavy client-side React packages that increase JS bundle sizes.
* **Our Solution:** A lightweight, zero-dependency package containing pre-configured React Server Components. It generates validated Organization, WebSite, and Article schemas and injects them directly into Next.js headers on the server.
* **GitHub Repo:** [next-seo-schema](https://github.com/Samiullah-Awan/next-seo-schema)

---

## The Growth Lessons We Learned
Publishing these tools taught us three key developer-marketing lessons:

1. **Solve Small, High-Value Friction Points:** Developers don't want a massive, closed platform for simple tasks. A clean, open-source script that solves one specific problem is highly shareable.
2. **Backlinks and Registry Authority:** Publishing packages on npm (npmjs.com) and PyPI (pypi.org) generates high-authority backlinks pointing back to your agency domain. These registries are crawled constantly, boosting our main site's search visibility.
3. **Show, Don't Tell:** Outbound sales pitches are easy to ignore. Sharing working code demonstrates our technical capabilities better than any sales deck.

---

## Scaling Your Digital Products
At **[The DIGIT](https://thedigithq.com)**, we build full-stack web applications, custom AI-powered workflows, and technical SEO setups. 

If you are looking to scale your engineering team, build a custom SaaS product, or optimize your platform's performance, let's collaborate. 

Check out our portfolio at **[thedigithq.com](https://thedigithq.com)**, or get in touch at **[business@thedigithq.com](mailto:business@thedigithq.com)**.
