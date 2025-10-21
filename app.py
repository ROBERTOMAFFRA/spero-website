from flask import Flask, render_template, send_from_directory
from flask_compress import Compress
from flask_talisman import Talisman
import os

app = Flask(__name__)
Compress(app)
Talisman(app, content_security_policy=None)

# ==================================================
#  MAINTENANCE MODE
# ==================================================
MAINTENANCE_MODE = os.getenv("MAINTENANCE_MODE", "False").lower() == "true"

@app.route('/')
def home():
    if MAINTENANCE_MODE:
        return render_template('maintenance.html')
    return render_template('index.html')

@app.route('/preview')
def preview():
    return render_template('index.html')

# ==================================================
#  SITEMAP ROUTE (SEO)
# ==================================================
@app.route('/sitemap.xml')
def sitemap():
    return render_template('sitemap_template.xml')

# ==================================================
#  LEGAL PAGES (NEW)
# ==================================================
@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# ==================================================
#  STATIC FILES (ICONS, IMAGES, ETC)
# ==================================================
@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'images/favicon.ico')

# ==================================================
#  ERROR HANDLERS
# ==================================================
@app.errorhandler(404)
def not_found_error(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# ==================================================
#  RUN
# ==================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
