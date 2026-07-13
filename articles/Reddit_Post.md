# I built two open-source developer tools to automate Google Indexing and on-page SEO. Here is the code and why I did it.

Hey r/webdev,

As web developers building SaaS products and marketing sites, we face the same indexing loop: you publish a new feature page or dynamic template, only to wait days or weeks for Google to discover it. Manual submissions in GSC are tedious.

To solve this for our team and clients, we built and open-sourced two simple developer utilities that automate GSC indexing and structured SEO schema injection.

Here is the breakdown of what we built and links to the repos.

---

## 1. Tool 1: GSC Fast Indexer (Python CLI)
* **The Pain Point:** Google takes forever to crawl new domains. Manual index requests inside GSC are limited to one URL at a time.
* **The Solution:** A Python CLI tool that uses Google's Indexing API to submit URLs in bulk. It parses local or remote `sitemap.xml` files, handles service account authentication, and requests crawling in seconds.
* **GitHub Link:** [gsc-fast-indexer on GitHub](https://github.com/Samiullah-Awan/gsc-fast-indexer)

---

## 2. Tool 2: React/Next.js SEO Schema Component Library
* **The Pain Point:** Injecting JSON-LD schema tags in React often requires heavy third-party packages that bloat your JS bundle sizes.
* **The Solution:** A lightweight, zero-dependency package containing pre-configured React Server Components. It generates and injects Organization, WebSite, and Article schemas into Next.js/React heads on the server.
* **GitHub Link:** [next-seo-schema on GitHub](https://github.com/Samiullah-Awan/next-seo-schema)

---

## Why Open Source?
We run **[The DIGIT](https://thedigithq.com)**, a digital product agency that builds SaaS applications and AI automations. 

We found that sharing tools openly is the best way to demonstrate our code quality, get feedback from other developers, and build authority.

Feel free to fork the code, submit pull requests, or use them in your own deployment pipelines! If you have any feedback or want to collaborate, check us out at **[thedigithq.com](https://thedigithq.com)** or get in touch at **[business@thedigithq.com](mailto:business@thedigithq.com)**.
