# linkedin-jobsearch-ai-agent  
A LinkedIn job-search automation tool that scrapes postings, filters results, removes duplicates, and generates a clean daily or weekly job digest.  
Fully configurable and cross-platform, suitable for beginners and developers alike.

---

## Features

- LinkedIn job scraping with automatic pagination  
- Keyword-based title and location filtering  
- Posting-age extraction (“Posted X days ago”)  
- Job deduplication using persistent job history  
- Markdown digest generation  
- Optional email notifications (Gmail App Password supported)  
- Configuration-driven design — no code changes needed  
- Extendable scraper architecture  
- Works on macOS, Linux, and Windows  
- Optional automation via launchd, cron, or Task Scheduler  

---

## Getting Started

### 1. Clone the repository
```
git clone https://github.com/tmtleung/linkedin-jobsearch-ai-agent.git
cd linkedin-jobsearch-ai-agent
```

### 2. Run the setup script

**macOS / Linux**
```
./setup.sh
```

If needed:
```
chmod +x setup.sh
./setup.sh
```

**Windows**
```
powershell -ExecutionPolicy Bypass -File setup.ps1
```

This will:
- create a virtual environment  
- install dependencies  
- create `config/config.json` from the example template  

---

## Configuring the Agent

Your main configuration file lives here:

```
config/config.json
```

It defines:

- job title keywords  
- location keywords  
- maximum posting age  
- email notification settings  
- LinkedIn scraper options  

Example:

```json
{
    "scrapers": {
        "linkedin": {
            "enabled": true,
            "keywords": ["Software Engineer", "Data Analyst", "Intern"],
            "location_keywords": ["Remote", "United States"],
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

## Customizing Your Location Search

The agent filters jobs by matching keywords inside the job’s location field.  
This allows users to target specific cities, states, regions, or countries.

### Modify in:
```
config/config.json
```

### Examples

**Search only in San Francisco:**
```json
"location_keywords": ["San Francisco"]
```

**Search multiple cities:**
```json
"location_keywords": ["Austin", "Seattle", "Denver"]
```

**Search a whole country:**
```json
"location_keywords": ["United States"]
```

**Search remote-only roles:**
```json
"location_keywords": ["Remote"]
```

**Remove location filtering entirely:**
```json
"location_keywords": []
```

### Why no radius setting?

LinkedIn’s public job listings do not provide a reliable radius parameter.  
City/region keyword matching works globally and avoids site-specific behavior.

---

## Running the Agent

After configuring:

```
python run_agent.py
```

The agent will:
1. Scrape LinkedIn  
2. Filter by title, location, and posting age  
3. Deduplicate using `history/job_history.json`  
4. Generate a Markdown digest in `outputs/latest_digest.md`  
5. Optionally email the digest  

---

## Optional: Email Digest Setup (Gmail)

1. Enable 2-Factor Authentication in Google  
2. Create an App Password  
3. Set the password as an environment variable:

**macOS / Linux**
```
export EMAIL_PASSWORD="your-app-password"
```

**Windows (PowerShell)**
```
setx EMAIL_PASSWORD "your-app-password"
```

Enable email:
```json
"email_notifications": { "enabled": true }
```

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

## Extending the Agent

Scrapers follow a simple interface:

```
scrapers/
    example_scraper_template.py
```

Each scraper must return jobs in this format:

```python
{
    "title": str,
    "company": str,
    "location": str,
    "url": str,
    "source": str
}
```

Adding additional sources (e.g., Indeed, Greenhouse, Lever) is straightforward.

---

## Project Structure

```
linkedin-jobsearch-ai-agent/
│
├── config/
│   ├── config.example.json
│   └── config.json
│
├── scrapers/
│   ├── linkedin_scraper.py
│   └── example_scraper_template.py
│
├── processor/
│   ├── filters.py
│   ├── relevance_classifier.py
│   └── dedupe.py
│
├── output/
│   ├── formatter.py
│   └── digest_builder.py
│
├── emailer/
│   └── mailer.py
│
├── utils/
│   ├── logger.py
│   └── html_utils.py
│
├── history/
│   └── .gitkeep
│
├── logs/
│   └── .gitkeep
│
├── outputs/
│   └── .gitkeep
│
├── docs/
│   ├── automation.md
│   └── filters.md
│
├── run_agent.py
├── setup.sh
├── setup.ps1
├── requirements.txt
└── LICENSE
```

---

## License
MIT License.

---

## Contributing
Pull requests are welcome.

