**🇮🇳 BharatInfo — Daily Intelligence Digest**

BharatInfo is a lightweight, static news and market intelligence dashboard focused on AI, business, Indian politics, Indian stocks, and global markets.

The project automatically collects news from RSS feeds, uses NewsAPI as a fallback, stores the daily digest as JSON, and publishes it through GitHub Pages. The frontend is built with plain HTML, CSS, and JavaScript, so no frontend framework or application server is required.

🌐 Live Demo

**Website: https://joel0005.github.io/bharatinfo/**

**Repository: https://github.com/joel0005/bharatinfo**

✨ **Features**

🤖 World AI — AI companies, tools, models, research, policy & ethics

💼 Corporate Business — Indian business, global business, startups & markets

🏛️ Indian Politics — central government, state politics, policy & elections

📊 Indian Stocks — market movers, IPOs, sectors and market news

🌐 World Stocks — US markets, Asian markets, commodities and crypto

📰 Automatic daily news aggregation from multiple RSS sources

🔄 NewsAPI fallback when an RSS category does not have enough articles

📅 Historical daily archive with date-based browsing

📈 Live market widgets using Yahoo Finance data through a public CORS proxy

⏱️ Market status indicator for NSE trading hours

🔁 Automatic stock refresh every 5 minutes

🔁 Automatic news refresh check every 15 minutes

🌍 Translation support for multiple Indian languages through Google Translate

✉️ Feedback form integration with Supabase

📱 Responsive layout for desktop and mobile

🚀 Automated data updates using GitHub Actions

🏗️ Architecture

                         ┌─────────────────────┐
                         │   RSS News Sources  │
                         └──────────┬──────────┘
                                    │
                                    ▼
┌──────────────────┐       ┌─────────────────────┐
│     NewsAPI      │──────▶│    fetch_news.py   │
│   fallback only  │       │  RSS + NewsAPI      │
└──────────────────┘       └──────────┬──────────┘
                                      │
                                      ▼
                            ┌───────────────────┐
                            │    docs/*.json    │
                            │ Today + archive   │
                            └─────────┬─────────┘
                                      │
                                      ▼
                            ┌───────────────────┐
                            │   GitHub Pages    │
                            │    index.html     │
                            └─────────┬─────────┘
                                      │
                 ┌────────────────────┼────────────────────┐
                 ▼                    ▼                    ▼
          News Dashboard       Stock Widgets       Feedback Form
                                  │                    │
                                  ▼                    ▼
                            Yahoo Finance          Supabase

Data flow

GitHub Actions starts the scheduled workflow.

fetch_news.py requests articles from configured RSS feeds.

Duplicate articles are removed by title.

If a subcategory contains fewer than 5 articles, NewsAPI is queried as a backup.

A maximum of 10 articles is stored for each subcategory.

**The generated digest is written to:**

docs/today.json

docs/YYYY-MM-DD.json

docs/archive.json

GitHub Actions commits and pushes the updated JSON files.

GitHub Pages serves the static website.

The browser loads the JSON data and renders the dashboard.

**📂 Project Structure**

bharatinfo/
│
├── .github/
│   └── workflows/
│       └── daily.yml          # Automated news-generation workflow
│
├── docs/
│   ├── index.html             # Main frontend application
│   ├── today.json             # Latest generated digest
│   ├── archive.json            # Available historical dates
│   └── YYYY-MM-DD.json        # Historical daily digest files
│
├── fetch_news.py              # RSS + NewsAPI data pipeline
│
└── README.md

📰 News Categories

**🤖 World AI**

Subcategory

Purpose

Company News

Major AI company developments

Tools & Platforms

AI products and platforms

Models

New AI/LLM model releases

Research

AI research and breakthroughs

Policy & Ethics

Regulation, governance and ethics

**💼 Corporate Business**

Subcategory

Purpose

India Business

Indian corporate developments

Global Business

International business news

Startups & Funding

Startup launches and funding

Markets & Economy

Business, economy and market developments

**🏛️ Indian Politics**

Subcategory

Purpose

Central Govt

Central government developments

State Politics

Indian state-level politics

Policy & Law

Government policy and legislation

Elections

Election-related news

**📊 Indian Stocks**

Subcategory

Purpose

Top Movers

Major Indian stock movements

IPO News

IPO and listing news

Sector News

Sector-specific developments

Market News

General Indian market news

**🌐 World Stocks**

Subcategory

Purpose

US Markets

S&P 500, Nasdaq, Dow and US market news

Asia Markets

Asian market developments

Commodities

Gold, silver and crude oil

Crypto

Bitcoin and other cryptocurrency news

**⚙️ Technology Stack**

Frontend

HTML5

CSS3

Vanilla JavaScript

Google Fonts

Google Translate

Backend / Data Pipeline

Python 3.11

requests

Python xml.etree.ElementTree for RSS parsing

JSON-based data storage

APIs / External Services

RSS feeds from multiple news publishers

NewsAPI — fallback news source

Yahoo Finance — market quotes

AllOrigins — CORS proxy for browser-side Yahoo Finance requests

Supabase — feedback storage

GitHub Actions — scheduled automation

GitHub Pages — hosting

**🚀 Run Locally**

1. Clone the repository

git clone https://github.com/joel0005/bharatinfo.git
cd bharatinfo

2. Install Python dependency

pip install requests

3. Configure NewsAPI

The script reads the API key from the NEWS_API_KEY environment variable.

Windows PowerShell

$env:NEWS_API_KEY="YOUR_NEWSAPI_KEY"
python fetch_news.py

Linux / macOS

export NEWS_API_KEY="YOUR_NEWSAPI_KEY"
python fetch_news.py

The generated files will be placed inside docs/.

Important: Never commit a real API key to the repository. Use environment variables locally and GitHub Secrets in Actions.

4. Preview the website

Because the frontend loads JSON files with fetch(), it is better to run a local HTTP server instead of opening index.html directly.

python -m http.server 8000 --directory docs

Then open:

http://localhost:8000

**🔐 GitHub Actions Setup
**
The workflow is located at:

.github/workflows/daily.yml

It uses the GitHub repository secret:

NEWS_API_KEY

Add the secret

Open the GitHub repository.

Go to Settings → Secrets and variables → Actions.

Create a new repository secret.

Set the name to:

NEWS_API_KEY

Paste your NewsAPI key as the value.

The workflow already passes the secret to Python:

env:
  NEWS_API_KEY: ${{ secrets.NEWS_API_KEY }}

The workflow can also be started manually using Actions → BharatInfo Daily Digest → Run workflow.

**⏰ Automated Update Schedule

The current GitHub Actions workflow runs six times per day using UTC cron expressions, corresponding to these IST times:

UTC

IST

23:30

5:00 AM

04:30

10:00 AM

06:30

12:00 PM

10:30

4:00 PM

12:30

6:00 PM

15:30

9:00 PM

The workflow fetches news, updates the JSON files, commits the changes, and pushes them back to the repository.

The website also performs a browser-side check for a newer today.json every 15 minutes, but this does not itself fetch new news from publishers. New news is generated when the GitHub Actions workflow runs.



**🌍 **Language Support

The interface includes Google Translate support for:

English

Hindi

Tamil

Telugu

Kannada

Marathi

Bengali

Gujarati

Malayalam

Punjabi**

The original article links remain available, and translated article links are generated through Google Translate when a non-English language is selected.

**✉️ Feedback System**

The feedback form in docs/index.html is designed to send submissions to a Supabase table named:

feedback

The frontend currently contains placeholders for:

const SUPABASE_URL = "https://YOUR_PROJECT.supabase.co";
const SUPABASE_KEY = "YOUR_ANON_KEY_HERE";

To enable feedback

Create a Supabase project.

**Create a feedback table with suitable columns such as:**

name

email

phone

message

Configure the required Row Level Security policies.

Replace the placeholder Supabase URL and anon key in docs/index.html.

Redeploy the GitHub Pages site.

Do not place a Supabase service-role key in the frontend. Only a properly restricted public/anon key should ever be exposed in browser code.

🗃️ JSON Data Format

A daily digest has the following high-level structure:

{
  "date": "YYYY-MM-DD",
  "date_nice": "Month DD, YYYY",
  "categories": [
    {
      "id": "ai",
      "label": "World AI",
      "emoji": "🤖",
      "subs": [
        {
          "id": "ai_company",
          "label": "Company News",
          "emoji": "🏢",
          "articles": [
            {
              "title": "Article title",
              "description": "Short description",
              "url": "https://example.com/article",
              "source": "example.com",
              "image": "https://example.com/image.jpg",
              "publishedAt": "2026-08-29T00:00:00Z"
            }
          ]
        }
      ]
    }
  ]
}

This keeps the frontend independent from the news collection process and makes historical archives easy to serve as static files.

🧹 Article Collection Logic

For each subcategory, BharatInfo:

Reads the configured RSS feeds.

Extracts title, description, URL, source, image and publication time.

Removes duplicate articles by title.

Removes [Removed] articles.

Sorts articles by publication timestamp.

If fewer than 5 articles are available, queries the configured NewsAPI backup query.

Keeps up to 10 articles for the subcategory.

This approach prioritizes RSS feeds and uses NewsAPI mainly as a backup, helping reduce API usage.

🗂️ Archive

Every generated digest is saved as a date-specific JSON file:

docs/2026-08-29.json
docs/2026-08-28.json
docs/2026-08-27.json
...

docs/archive.json maintains the list of available dates. The frontend reads this file to build the archive navigation.

The Python pipeline keeps the newest 90 archive entries.

**🚢 Deployment**

The project is designed for GitHub Pages.

GitHub Pages

Push the repository to GitHub.

Open Settings → Pages.

Select GitHub Actions as the deployment/source method, or configure Pages to serve the docs directory according to your repository setup.

Ensure the generated site is available at your GitHub Pages URL.

The current live deployment is:

https://joel0005.github.io/bharatinfo/

**🔒 Security Notes**

Keep NEWS_API_KEY in GitHub Secrets.

Never hard-code private API keys in fetch_news.py or commit them to Git.

The frontend can expose a Supabase anon/public key, but the database must be protected with appropriate Row Level Security policies.

Do not expose a Supabase service-role key in index.html.

Market data is fetched through third-party services and should be treated as informational.

News articles belong to their respective publishers; BharatInfo stores metadata and links back to the original sources.

⚠️ Current Limitations

RSS feed availability can change when publishers modify or remove feeds.

Some RSS feeds may return fewer articles than expected.

NewsAPI is used only as a fallback and is subject to its plan limits.

Browser-side market data depends on Yahoo Finance and the AllOrigins proxy being available.

Market quotes may be delayed and are not guaranteed to be tick-by-tick.

Google Translate output is machine-generated and may not perfectly preserve the meaning of the original article.

The feedback feature requires Supabase configuration before it can store submissions.

The current repository does not define a software license.

**🛣️ Future Improvements
**
Possible next steps for BharatInfo include:

Add source-level health monitoring for RSS feeds.

Add stronger article relevance filtering per category.

Add smarter duplicate detection beyond exact title matching.

Add search across historical news.

Add market charts and historical price data.

Add personalized watchlists.

Add push/email notifications for important stories.

Add a backend/API layer for more reliable market data.

Add automated tests for the news pipeline.

Add CI checks for malformed JSON and broken feeds.

Improve accessibility and keyboard navigation.

Add source attribution and data-quality indicators to each article.

**🤝 Contributing**

Contributions and suggestions are welcome.

A typical workflow is:

git checkout -b feature/your-feature
git add .
git commit -m "Add your feature"
git push origin feature/your-feature

Then open a pull request on GitHub.


**❤️ About BharatInfo**

BharatInfo is built as a simple daily intelligence dashboard for India, bringing important developments across technology, business, politics, and markets into one place.

AI · Business · Politics · Stocks

Built with ❤️ in India.
