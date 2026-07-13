# Implementing Dynamic JSON-LD Schema in Next.js App Router

Structured data is a cornerstone of technical SEO. By injecting JSON-LD (JavaScript Object Notation for Linked Data) schemas into your HTML, you help search engine crawlers understand your site structure, content, and organization. This directly leads to rich snippets, star ratings, and Google Knowledge Panel placements.

In the Next.js App Router environment, implementing these schemas requires leveraging React Server Components (RSC) to ensure the structured data is present on the initial page load.

In this tutorial, we will construct a reusable React component that generates dynamic Organization and Article schemas.

---

## 🛠️ Step 1: Designing the Schema Component
Since Server Components render on the server and send zero client-side JavaScript, we can write a simple component that injects a `<script>` tag:

```tsx
import React from 'react';

interface OrgProps {
  name: string;
  url: string;
  logo: string;
  sameAs?: string[];
}

export function OrganizationSchema({ name, url, logo, sameAs = [] }: OrgProps) {
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

## 🚀 Step 2: Consuming in Next.js App Router
Because our component is a standard Server Component, using it inside a Next.js layout or page is extremely clean:

```tsx
import { OrganizationSchema } from './components/OrganizationSchema';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <OrganizationSchema 
          name="The DIGIT"
          url="https://thedigithq.com"
          logo="https://thedigithq.com/logo.png"
          sameAs={[
            "https://x.com/thedigithq",
            "https://github.com/Samiullah-Awan"
          ]}
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

This injects the schema directly into the document `<head>` on initial render, ensuring crawler bots capture it immediately without waiting for client-side JavaScript execution.

---

## 📦 Open Source Library
If you want to use a fully tested, pre-configured component library for Next.js SEO, check out our package:
👉 **[next-seo-schema on GitHub](https://github.com/Samiullah-Awan/next-seo-schema)**

---

## Technical Engineering Services
This component was built by **[The DIGIT](https://thedigithq.com)**, a remote-first digital product agency. 

We build and scale high-performance Next.js platforms, React applications, and custom AI automations. If you need help optimising your application’s core web vitals, dynamic sitemaps, or custom components, reach out to our team at **[thedigithq.com](https://thedigithq.com)** or email us at **[business@thedigithq.com](mailto:business@thedigithq.com)**.
