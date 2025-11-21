"""
Example scraper template for extending the JobSearch AI Agent.

Every scraper must implement:

    def run(config) -> List[dict]

It should return a list of job dictionaries with fields:

    {
        "title": str,
        "company": str,
        "location": str,
        "url": str,
        "source": str
    }

This template is fully commented to guide new scraper authors.
"""

from typing import List, Dict


def run(config) -> List[Dict]:
    """
    Your scraping logic goes here.

    The agent pipeline will call this function and expect
    a list of job dictionaries following the required schema.
    """

    jobs = []

    # Example structure:
    #
    # jobs.append({
    #     "title": "Example Job Title",
    #     "company": "Example Company",
    #     "location": "Remote",
    #     "url": "https://example.com/job",
    #     "source": "example"
    # })

    return jobs
