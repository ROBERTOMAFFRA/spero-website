# ======================================================
# SPERO RESTORATION - AI SITEMAP GENERATOR
# ======================================================

import os
import openai
from datetime import datetime
from config import Config

# Load API key
openai.api_key = Config.OPENAI_API_KEY

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "sitemap.xml")

def generate_ai_description(url):
    """Generates a short SEO description for each page using OpenAI."""
    try:
        prompt = f"Write a concise SEO description (max 150 chars) for a page about {url} from Spero Restoration in Orlando."
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=80,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI Error on {url}: {e}")
        return "Professional restoration services by Spero Restoration."

def build_sitemap():
    """Creates sitemap.xml with AI-enhanced metadata."""
    print("🔧 Generating AI-powered sitemap...")

    urls = [
        f"{Config.DOMAIN}/",
        f"{Config.DOMAIN}/contact",
        f"{Config.DOMAIN}/blog",
        f"{Config.DOMAIN}/thank-you"
    ]

    # Add blog posts
    blog_dir = os.path.join(os.path.dirname(__file__), "..", "blog_content")
    if os.path.exists(blog_dir):
        for file in os.listdir(blog_dir):
            if file.endswith(".md"):
                slug = file.replace(".md", "")
                urls.append(f"{Config.DOMAIN}/blog/{slug}")

    # Generate sitemap entries
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for url in urls:
        description = generate_ai_description(url)
        xml.append("  <url>")
        xml.append(f"    <loc>{url}</loc>")
        xml.append(f"    <lastmod>{datetime.utcnow().date()}</lastmod>")
        xml.append("    <changefreq>weekly</changefreq>")
        xml.append("    <priority>0.8</priority>")
        xml.append(f"    <data:display>{description}</data:display>")
        xml.append("  </url>")

    xml.append("</urlset>")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(xml))

    print(f"✅ Sitemap generated successfully: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_sitemap()
