# linkedin-jobsearch-ai-agent  
Automated LinkedIn job scraper that filters, deduplicates, and emails clean job digests.  
A simple, configurable, cross-platform job-search automation tool.

This project is designed so **anyone** (even beginners) can run an automated job search using:
- a single editable config file  
- a built-in LinkedIn scraper  
- optional email notifications  
- optional automation (macOS, Windows, Linux)  

No coding experience required.

---

## Features

- LinkedIn job scraping with dynamic pagination  
- Keyword-based title and location filtering  
- Posting-age extraction (“Posted X days ago”)  
- Deduplication with persistent job history  
- Clean Markdown digest output  
- Optional email notifications (Gmail app password supported)  
- Configuration-only workflow  
- Extendable scraper architecture  
- Cross-platform automation support:
  - macOS (launchd)
  - Linux (cron)
  - Windows (Task Scheduler)

---

## Quick Start

### 1. Clone the repository
```
git clone https://github.com/yourusername/linkedin-jobsearch-ai-agent.git
cd linkedin-jobsearch-ai-agent
```

### 2. Create a virtual environment

**macOS / Linux**
```
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Copy the example config
```
cp config/config.example.json config/config.json
```

### 5. Edit your config  
Open:

```
config/config.json
```

Set:
- job title keywords  
- location keywords  
- max posting age  
- email settings (optional)  
- LinkedIn scraper options  

No code modifications required.

---

## Optional: Email Digest Setup (Gmail)

If you want automatic email digests:

1. Enable 2-Factor Authentication in Google  
2. Create an App Password  
3. Set it as an environment variable:

**macOS / Linux**
```
export EMAIL_PASSWORD="your-16-char-app-password"
```

**Windows**
```
setx EMAIL_PASSWORD "your-16-char-app-password"
```

Enable email in `config.json`:
```json
"email_notifications": {
    "enabled": true
}
```

---

## Running the Agent

Run manually:

```
python run_agent.py
```

The agent will:
1. Scrape LinkedIn  
2. Filter and classify results  
3. Deduplicate against job history  
4. Generate a Markdown digest  
5. Send an email (if enabled)  
6. Save output into `outputs/latest_digest.md`

---

## Automation (macOS, Linux, Windows)

See:
```
docs/automation.md
```

Includes step-by-step instructions for:

- macOS launchd  
- Linux cron  
- Windows Task Scheduler  

---

## Configuration Overview

### Located in:
```
config/config.json
```

### Example structure:
```json
{
    "scrapers": {
        "linkedin": {
            "enabled": true,
            "keywords": ["Software Engineer", "Data Analyst", "Intern"],
            "location_keywords": ["Remote", "New York", "USA"],
            "max_pages": 10
        }
    },

    "filters": {
        "max_post_age_days": 30
    },

    "email_notifications": {
        "enabled": false,
        "sender": "youremail@example.com",
        "recipients": ["youremail@example.com"],
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 587,
        "use_tls": true,
        "subject_template": "Job Digest — {{date}}"
    }
}
```

---

## Extending the Agent

To add additional job boards, see:

```
scrapers/example_scraper_template.py
```

Any scraper must return job dictionaries in this format:

```python
{
    "title": str,
    "company": str,
    "location": str,
    "url": str,
    "source": str
}
```

---

## Project Structure

```
linkedin-jobsearch-ai-agent/
│
├── config/
│   ├── config.json               # User-provided settings
│   └── config.example.json       # Public template
│
├── scrapers/
│   ├── linkedin_scraper.py       # Fully implemented LinkedIn scraper
│   └── example_scraper_template.py
│
├── processor/
│   ├── filters.py                # Title/location/date filtering
│   ├── relevance_classifier.py   # Classification logic
│   └── dedupe.py                 # Job history deduplication
│
├── output/
│   ├── formatter.py              # Job line formatting
│   └── digest_builder.py         # Markdown digest builder
│
├── emailer/
│   └── mailer.py                 # Gmail SMTP email sender
│
├── utils/
│   ├── logger.py                 # Unified logger
│   └── html_utils.py             # HTML parsing helpers
│
├── history/
│   └── .gitkeep                  # Keeps folder versioned
│
├── logs/
│   └── .gitkeep                  # Keeps folder versioned
│
├── outputs/
│   └── .gitkeep                  # Digest output folder
│
├── docs/
│   ├── automation.md             # OS scheduling instructions
│   └── filters.md                # Filter customization guide
│
├── run_agent.py                  # Main entry point
├── requirements.txt              # Python dependencies
└── LICENSE                       # MIT license
```

---

## License
MIT License.  
Free for personal and commercial use.

---

## Contributing  
Pull requests welcome.

