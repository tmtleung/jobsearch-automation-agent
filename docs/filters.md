# Filter Logic Guide

The agent filters job postings by title, location, and posting age.

---

## Title Filtering

Jobs match when their title contains any token in:

```
scrapers.linkedin.keywords
```

Examples:
```
["Software Engineer", "Data Analyst", "Intern"]
```

Partial matches are allowed:
- “Senior Software Engineer”
- “Data Analyst I”
- “Software Engineering Intern”

---

## Location Filtering

Jobs match when the job’s location contains any keyword in:

```
scrapers.linkedin.location_keywords
```

Examples:
```
["Remote", "New York", "USA"]
```

Case-insensitive.

---

## Posting Age Filtering

LinkedIn formats include:
- “Posted today”
- “Posted 1 day ago”
- “Posted X days ago”
- “Just posted”

The agent excludes postings older than:
```
filters.max_post_age_days
```

---

## Customizing Filters

Users can:
1. Modify keywords in `config/config.json`  
2. Adjust max post age  
3. Add custom logic in `processor/filters.py`  
