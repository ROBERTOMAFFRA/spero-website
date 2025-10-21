from flask import Flask, render_template, request, jsonify, url_for, abort, make_response
from flask_compress import Compress
from flask_talisman import Talisman
from datetime import datetime
import os

# --- Inicialização do app ---
app = Flask(__name__)
Compress(app)
Talisman(app, content_security_policy=None)

# --- Variável de controle de manutenção ---
MAINTENANCE_MODE = True  # 🔒 alterar para False para liberar o site

# --- Rotas principais ---
@app.before_request
def check_maintenance_mode():
    # Permite acessar o /preview mesmo com modo manutenção ativo
    if MAINTENANCE_MODE and request.path != "/preview":
        resp = make_response(render_template("maintenance.html", current_year=datetime.now().year), 503)
        resp.headers["Retry-After"] = "86400"  # 24 horas
        return resp

@app.route("/")
def index():
    return render_template("index.html", current_year=datetime.now().year)

@app.route("/privacy")
def privacy():
    return render_template("privacy.html", current_year=datetime.now().year)

@app.route("/terms")
def terms():
    return render_template("terms.html", current_year=datetime.now().year)

@app.route("/admin")
def admin():
    return render_template("admin.html", current_year=datetime.now().year)

@app.route("/preview")
def preview():
    """
    🔍 Rota especial para visualização do site mesmo em modo manutenção.
    Acesse https://spero-restoration.com/preview
    """
    return render_template("index.html", current_year=datetime.now().year)

# --- Formulário de envio ---
@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.get_json()
    print("=== New Website Lead ===")
    print(f"Name: {data.get('name')}")
    print(f"Email: {data.get('email')}")
    print(f"Phone: {data.get('phone')}")
    print(f"Service: {data.get('service')}")
    print(f"Message: {data.get('message')}")
    print("=========================")
    return jsonify({"status": "success", "message": "Form submitted successfully."})

# --- Sitemap dinâmico ---
@app.route("/sitemap.xml")
def sitemap():
    pages = [
        {"loc": url_for("index", _external=True)},
        {"loc": url_for("privacy", _external=True)},
        {"loc": url_for("terms", _external=True)},
        {"loc": url_for("admin", _external=True)},
    ]
    template = render_template("sitemap_template.xml", pages=pages, lastmod=datetime.now().date())
    resp = make_response(template)
    resp.headers["Content-Type"] = "application/xml"
    return resp

# --- Robots.txt dinâmico ---
@app.route("/robots.txt")
def robots():
    content = (
        "User-agent: *\n"
        "Disallow: /\n"  # bloqueia indexação enquanto em manutenção
        "Sitemap: https://spero-restoration.com/sitemap.xml"
    )
    resp = make_response(content)
    resp.headers["Content-Type"] = "text/plain"
    return resp

# --- Erros personalizados ---
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", current_year=datetime.now().year), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html", current_year=datetime.now().year), 500

# --- Execução local ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
