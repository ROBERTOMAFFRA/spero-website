# ======================================================
# SPERO RESTORATION - MAIN ROUTES
# ======================================================

from flask import Blueprint, render_template, request
from config import Config

main_bp = Blueprint("main", __name__)

# ------------------------------------------------------
# HOME PAGE
# ------------------------------------------------------
@main_bp.route("/")
def index():
    lang = request.args.get("lang", "en")
    meta = {
        "title": "Spero Restoration | Water Damage, Mold & Fire Restoration in Orlando",
        "description": "Spero Restoration offers professional water damage repair, mold removal, and fire restoration services across Orlando. 24/7 emergency response.",
        "url": f"{Config.DOMAIN}/?lang={lang}",
        "image": "/static/images/banner.webp",
    }
    return render_template("index.html", meta=meta, lang=lang)

# ------------------------------------------------------
# ABOUT PAGE (optional route)
# ------------------------------------------------------
@main_bp.route("/about")
def about():
    lang = request.args.get("lang", "en")
    meta = {
        "title": "About Spero Restoration | Experienced Restoration Experts",
        "description": "Learn more about Spero Restoration's experience, mission, and commitment to excellence in restoration services.",
        "url": f"{Config.DOMAIN}/about?lang={lang}",
    }
    return render_template("index.html", scroll_to="about", meta=meta, lang=lang)

# ------------------------------------------------------
# SERVICES PAGE (optional route)
# ------------------------------------------------------
@main_bp.route("/services")
def services():
    lang = request.args.get("lang", "en")
    meta = {
        "title": "Our Services | Water, Mold & Fire Restoration in Orlando",
        "description": "Explore our professional restoration services — water damage repair, mold remediation, and fire recovery for homes and businesses.",
        "url": f"{Config.DOMAIN}/services?lang={lang}",
    }
    return render_template("index.html", scroll_to="services", meta=meta, lang=lang)

# ------------------------------------------------------
# LANGUAGE SELECTOR
# ------------------------------------------------------
@main_bp.route("/lang/<lang_code>")
def switch_language(lang_code):
    if lang_code not in Config.SUPPORTED_LANGUAGES:
        lang_code = "en"
    return render_template("index.html", lang=lang_code)
