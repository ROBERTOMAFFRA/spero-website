from flask import Flask, render_template, send_from_directory
from flask_compress import Compress
from flask_talisman import Talisman
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
Compress(app)
Talisman(app, content_security_policy=None)

# ====== CONFIGURAÇÕES ======
MAINTENANCE_MODE = True  # Altere para False quando quiser liberar o site
CONTACT_EMAIL = "contact@spero-restoration.com"
CONTACT_PHONE = "(407) 724-6310"


# ====== ROTAS ======
@app.route("/")
def index():
    if MAINTENANCE_MODE:
        return render_template("maintenance.html", phone=CONTACT_PHONE, email=CONTACT_EMAIL)
    return render_template("index.html", phone=CONTACT_PHONE, email=CONTACT_EMAIL)


@app.route("/preview")
def preview():
    """Permite visualizar o site mesmo em modo manutenção"""
    return render_template("index.html", phone=CONTACT_PHONE, email=CONTACT_EMAIL)


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/sitemap.xml")
def sitemap():
    return render_template("sitemap_template.xml"), 200, {"Content-Type": "application/xml"}


@app.route("/robots.txt")
def robots():
    return send_from_directory(app.static_folder, "robots.txt")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
