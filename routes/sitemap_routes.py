# ======================================================
# SPERO RESTORATION - SITEMAP & ROBOTS ROUTES
# ======================================================

from flask import Blueprint, Response
from config import Config
import os
from datetime import datetime

sitemap_bp = Blueprint("sitemap", __name__)

# ------------------------------------------------------
# DYNAMIC SITEMAP GENERATION
# ------------------------------------------------------
@sitemap_bp.route("/sitemap.xml", methods=["GET"])
def sitemap():
    pages = [
        {"loc": f"{Config.DOMAIN}/", "priority": "1.0"},
        {"loc": f"{Config.DOMAIN}/contact", "priority": "0.9"},
        {"loc": f"{Config.DOMAIN}/blog", "priority": "0.8"},
        {"loc": f"{Config.DOMAIN}/thank-you", "priority": "0.5"},
    ]

    # Include all blog articles automatically
    blog_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "blog_content")
    if os.path.exists(blog_dir):
        for file in os.listdir(blog_dir):
            if file.endswith(".md"):
                slug = file.replace(".md", "")
                pages.append({
                    "loc": f"{Config.DOMAIN}/blog/{slug}",
                    "priority": "0.7"
                })

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for page in pages:
        xml.append("  <url>")
        xml.append(f"    <loc>{page['loc']}</loc>")
        xml.append(f"    <lastmod>{datetime.utcnow().date()}</lastmod>")
        xml.append(f"    <changefreq>weekly</changefreq>")
        xml.append(f"    <priority>{page['priority']}</priority>")
        xml.append("  </url>")

    xml.append("</urlset>")
    sitemap_xml = "\n".join(xml)

    return Response(sitemap_xml, mimetype="application/xml")


# ------------------------------------------------------
# ROBOTS.TXT
# ------------------------------------------------------
@sitemap_bp.route("/robots.txt", methods=["GET"])
def robots():
    content = f"""User-agent: *
Disallow:

Sitemap: {Config.DOMAIN}/sitemap.xml
"""
    return Response(content, mimetype="text/plain")
