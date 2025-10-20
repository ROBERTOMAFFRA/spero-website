# ================================================================
# SPERO RESTORATION vFinal – SEO MASTER PLAN
# Full WebApp Flask Structure with Multilingual Routing
# ================================================================

from flask import Flask, render_template, send_from_directory
from dotenv import load_dotenv
import os

# ------------------------------------------------------------
# 1️⃣ INITIAL SETUP
# ------------------------------------------------------------
load_dotenv()
app = Flask(__name__)

# ------------------------------------------------------------
# 2️⃣ HOME ROUTES (Multilingual)
# ------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/es/')
def index_es():
    return render_template('index-es.html')

@app.route('/pt/')
def index_pt():
    return render_template('index-pt.html')


# ------------------------------------------------------------
# 3️⃣ STATIC & MEDIA FILES
# ------------------------------------------------------------
@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt', mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml', mimetype='application/xml')


# ------------------------------------------------------------
# 4️⃣ CUSTOM ERROR HANDLERS
# ------------------------------------------------------------
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(503)
def maintenance_mode(error):
    return render_template('503.html'), 503


# ------------------------------------------------------------
# 5️⃣ LAUNCH
# ------------------------------------------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
