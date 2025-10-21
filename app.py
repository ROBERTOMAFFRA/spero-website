from flask import Flask, render_template, send_from_directory, make_response
from flask_compress import Compress
from flask_talisman import Talisman
import os
from datetime import datetime

# ==================================================
# INITIAL CONFIGURATION
# ==================================================
app = Flask(__name__, static_folder="static", template_folder="templates")

# Performance and Security Enhancements
Compress(app)
Talisman(
    app,
    content_security_policy=None,
    force_https=True,
    strict_transport_security=True,
)

# ==================================================
# GLOBAL VARIABLES
# ==================================================
MAINTENANCE_MODE = os.getenv("MAINTENANCE_MODE", "False").lower() == "true"

# ==================================================
# MAIN ROUTES
# ==================================================
@app.route("/")
def home():
    if MAINTENANCE_MODE:
        return render_template("maintenance.html")
    return render_template("index.html")

@app.route("/preview")
def preview():
    # For internal use (bypasses maintenance mode)
    return render_template("index.html")

# ==================================================
# LEGAL ROUTES
# ==================================================
@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

# ==================================================
# SITEMAP & ROBOTS (SEO)
# ==================================================
@app.route("/sitemap.xml")
def sitemap():
    pages = [
        {"loc": "https://spero-restoration.com/"},
        {"loc": "https://spero-restoration.com/terms"},
        {"loc": "https://spero-restoration.com/privacy"},
    ]
    sitemap_xml = render_template("sitemap_template.xml", pages=pages, lastmod=datetime.now().date())
    resp = make_response(sitemap_xml)
    resp.headers["Content-Type"] = "application/xml"
    return resp

@app.route("/robots.txt")
def robots():
    return send_from_directory(app.static_folder, "robots.txt")

# ==================================================
# STATIC FILES
# ==================================================
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(app.static_folder, "images/favicon.ico")

# ==================================================
# ERROR HANDLERS
# ==================================================
@app.errorhandler(404)
def not_found_error(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500

# ==================================================
# RUN
# ==================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
