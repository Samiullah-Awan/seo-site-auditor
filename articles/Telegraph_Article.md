# How to Setup Google Indexing API in 3 Steps

When you launch a new web page, waiting for Google to index it naturally can take weeks. Using the **Google Indexing API** allows you to request instant crawling, reducing indexing times to minutes.

Here is the quick, 3-step setup guide.

---

### Step 1: Enable the API & Create a Service Account
1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and search for the **Google Indexing API**, then click **Enable**.
3. Go to **IAM & Admin** > **Service Accounts** and click **Create Service Account**.
4. Generate a **JSON key** for your new Service Account, download it, and rename it to `credentials.json`. Copy the Service Account email address.

---

### Step 2: Grant Owner Access in Google Search Console
Google needs to verify that your Service Account has permission to request indexing for your site:
1. Open [Google Search Console](https://search.google.com/search-console).
2. Navigate to **Settings** > **Users and permissions**.
3. Click **Add User**, paste the Service Account email, and set the permission to **Owner**.

---

### Step 3: Run the Indexing Script
Use a simple Python script to push your URLs directly to Google's indexing queue:

```python
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

credentials = service_account.Credentials.from_service_account_file(
    'credentials.json', 
    scopes=['https://www.googleapis.com/auth/indexing']
)
session = AuthorizedSession(credentials)

payload = {
    "url": "https://thedigithq.com",
    "type": "URL_UPDATED"
}
response = session.post(
    "https://indexing.googleapis.com/v3/urlNotifications:publish", 
    json=payload
)
print(response.json())
```

For a pre-configured version of this CLI tool supporting sitemaps and text files, download the open-source client:
👉 **[Samiullah-Awan/gsc-fast-indexer on GitHub](https://github.com/Samiullah-Awan/gsc-fast-indexer)**

---

### Technical SEO Support
Need help implementing automated sitemaps, Next.js rendering, or programmatic SEO configurations? 

Partner with the engineering experts at **[The DIGIT](https://thedigithq.com)**. Contact us at **[business@thedigithq.com](mailto:business@thedigithq.com)** or visit **[thedigithq.com](https://thedigithq.com)**.
