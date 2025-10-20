# ======================================================
# SPERO RESTORATION - BLOG ROUTES
# ======================================================

from flask import Blueprint, render_template, request, abort
from config import Config
import os
import markdown
from datetime import datetime

blog_bp = Blueprint("blog", __name__)

BLOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "blog_content")

# ------------------------------------------------------
# LIST ALL BLOG ARTICLES
# ------------------------------------------------------
@blog_bp.route("/blog")
def blog_home():
    articles = []
    for file in os.listdir(BLOG_DIR):
        if file.endswith(".md"):
            file_path = os.path.join(BLOG_DIR, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                title = content.splitlines()[0].replace("#", "").strip()
                slug = file.replace(".md", "")
                articles.append({
                    "title": title,
                    "slug": slug,
                    "url": f"/blog/{slug}",
                })
    meta = {
        "title": "Blog | Spero Restoration Orlando",
        "description": "Tips, guides, and insights on water damage, mold remediation, and fire restoration — by Spero Restoration.",
        "url": f"{Config.DOMAIN}/blog"
    }
    return render_template("blog.html", articles=articles, meta=meta)


# ------------------------------------------------------
# DISPLAY A SPECIFIC ARTICLE
# ------------------------------------------------------
@blog_bp.route("/blog/<slug>")
def blog_article(slug):
    file_path = os.path.join(BLOG_DIR, f"{slug}.md")
    if not os.path.exists(file_path):
        abort(404)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        html_content = markdown.markdown(content, extensions=["fenced_code", "tables"])

    # SEO Meta
    meta = {
        "title": f"{slug.replace('-', ' ').title()} | Spero Restoration Blog",
        "description": f"Learn about {slug.replace('-', ' ')} from the experts at Spero Restoration in Orlando.",
        "url": f"{Config.DOMAIN}/blog/{slug}"
    }
    return render_template("article.html", content=html_content, meta=meta)
