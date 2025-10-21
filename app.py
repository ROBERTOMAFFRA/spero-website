from flask import Flask, render_template, request, jsonify, Response, url_for
import os
from dotenv import load_dotenv
from flask_compress import Compress
from flask_talisman import Talisman

# ------------------------------------
# Inicialização
# ------------------------------------
load_dotenv()
app = Flask(__name__)

# Compressão GZIP + Brotli
Compress(app)

# Segurança e SEO Headers
Talisman(
    app,
    content_security_policy={
        "default-src": "'self'",
        "img-src": "'self' data: https://www.googletagmanager.com https://www.google-analytics.com",
        "script-src": "'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com",
        "style-src": "'self' 'unsafe-inline'",
        "connect-src": "'self' https://www.google-analytics.com",
        "frame-src": "https://www.googletagmanager.com"
    },
    force_https=True
)

# ------------------------------------
# Rotas principais
# ------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

# ------------------------------------
# API: formulário de contato
# ------------------------------------
@app.route("/send_message", methods=["POST"])
def send_message():
    name = request.form.get("name", "")
    email = request.form.get("email", "")
    phone = request.form.get("phone", "")
    service = request.form.get("service", "")
    message = request.form.get("message", "")

    # Log básico (futuro: integração com SendGrid)
    print("=== New Website Lead ===")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Phone: {phone}")
    print(f"Service: {service}")
    print(f"Message: {message}")
    print("========================")

    return jsonify({"status": "success", "message": "Form submitted successfully."}), 200

# ------------------------------------
# SEO: Sitemap dinâmico e Robots.txt
# ------------------------------------
@app.route("/sitemap.xml")
def sitemap_xml():
    pages = [
        url_for('home', _external=True),
        url_for('privacy', _external=True),
        url_for('terms', _external=True),
    ]
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for p in pages:
        xml.append(f"<url><loc>{p}</loc></url>")
    xml.append("</urlset>")
    return Response("\n".join(xml), mimetype="application/xml")

@app.route("/robots.txt")
def robots_txt():
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Sitemap: https://spero-restoration.com/sitemap.xml\n"
    )
    return Response(content, mimetype="text/plain")

# ------------------------------------
# Healthcheck (Render e Monitoramento)
# ------------------------------------
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

# ------------------------------------
# Tratamento de erros
# ------------------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

@app.errorhandler(503)
def maintenance(e):
    return render_template("maintenance.html"), 503

# ------------------------------------
# Execução local
# ------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
