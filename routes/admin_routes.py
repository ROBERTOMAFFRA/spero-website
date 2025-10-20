# ======================================================
# SPERO RESTORATION - ADMIN ROUTES
# ======================================================

from flask import Blueprint, render_template, jsonify
from datetime import datetime
import os

admin_bp = Blueprint("admin", __name__)

# ------------------------------------------------------
# DASHBOARD - BASIC STATS VIEW
# ------------------------------------------------------
@admin_bp.route("/admin/dashboard")
def dashboard():
    # Simulated stats (later these can be connected to GA or HubSpot)
    stats = {
        "visits_today": 128,
        "form_submissions": 6,
        "blog_posts": len(os.listdir(os.path.join(os.path.dirname(__file__), "..", "blog_content"))),
        "last_backup": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    }
    meta = {
        "title": "Admin Dashboard | Spero Restoration",
        "description": "Internal dashboard with key metrics and performance overview for Spero Restoration.",
        "url": "https://spero-restoration.com/admin/dashboard"
    }
    return render_template("admin_dashboard.html", stats=stats, meta=meta)

# ------------------------------------------------------
# API ENDPOINT (OPTIONAL)
# ------------------------------------------------------
@admin_bp.route("/api/stats")
def api_stats():
    data = {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }
    return jsonify(data)
