# ======================================================
# SPERO RESTORATION - COMPETITOR SEO SCANNER
# ======================================================

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# List of competitors in the Orlando area
COMPETITORS = [
    "https://www.servproorlando.com/",
    "https://www.puroclean.com/orlando-fl/",
    "https://www.restoration1.com/orlando/",
    "https://www.belfor.com/en/us/belfor-usa/offices/orlando",
]

REPORT_FILE = "competitor_report.txt"


def fetch_keywords(url):
    """Fetch title, meta description and common keywords from competitor site"""
    print(f"🔍 Scanning: {url}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string.strip() if soup.title else ""
        desc = soup.find("meta", attrs={"name": "description"})
        desc = desc["content"].strip() if desc and "content" in desc.attrs else ""

        # Extract frequent words (excluding stopwords)
        text = soup.get_text(separator=" ").lower()
        words = re.findall(r"\b[a-z]{4,}\b", text)
        common = {}
        for w in words:
            common[w] = common.get(w, 0) + 1

        keywords = sorted(common, key=common.get, reverse=True)[:30]
        return title, desc, keywords
