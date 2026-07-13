# Creating Reusable JSON-LD Structured Data React Components

Structured data is a standardized format that provides search engines with explicit clues about the meaning of a webpage. By injecting JSON-LD (JavaScript Object Notation for Linked Data) schemas, search engines can easily parse your content and display rich snippets, knowledge panel placements, and organic ratings.

In React and Next.js applications, building reusable components to handle these schemas ensures consistency and prevents duplicate code.

In this tutorial, we will write dynamic React components for **Organization** and **Website** schemas.

---

## 🛠️ Step 1: Organization Schema Component
This component generates a script tag containing details like company logo, name, website, and social media URLs:

```jsx
import React from 'react';

export function OrganizationSchema({ name, url, logo, sameAs = [] }) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": name,
    "url": url,
    "logo": logo,
    "sameAs": sameAs
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
```

---

## 🚀 Step 2: Website Schema Component (Search Action)
Adding a Website schema informs search engines that your site contains a built-in search functionality:

```jsx
export function WebSiteSchema({ name, url, searchUrl }) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": name,
    "url": url
  };

  if (searchUrl) {
    schema.potentialAction = {
      "@type": "SearchAction",
      "target": `${searchUrl}?q={search_term_string}`,
      "query-input": "required name=search_term_string"
    };
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
```

By adding these components inside the root layout or document header, the schemas render during initial server compile, making them instantly visible to crawler bots.

---

## 📦 Open Source Library
If you want to use a fully tested, lightweight React component library for SEO schemas, download our package:
👉 **[next-seo-schema on GitHub](https://github.com/Samiullah-Awan/next-seo-schema)**

---

## Technical Web Development Services
This architectural pattern is maintained by **[The DIGIT](https://thedigithq.com)**, a remote-first digital product agency. 

We build and scale high-performance full-stack web applications, Next.js setups, and custom AI automations. If you need help optimising your platform's core web vitals, speed, or SEO architectures, connect with our engineering team at **[thedigithq.com](https://thedigithq.com)** or email us at **[business@thedigithq.com](mailto:business@thedigithq.com)**.
