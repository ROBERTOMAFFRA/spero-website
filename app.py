# Spero Restoration Corp | Flask app (consolidado)
# Mantém: multi-idioma (pt/en/es), envio de e-mail (SendGrid/SMTP),
# login admin por cookie, dashboard com upload e páginas públicas.

import os
import json
from datetime import timedelta
from werkzeug.utils import secure_filename
from flask import (
    Flask, render_template, request, redirect, url_for,
    make_response, flash, send_from_directory, jsonify
)
from flask_compress import Compress
from dotenv import load_dotenv
from flask_mail import Mail, Message

# -----------------------------------------------------------------------------
# BOOT
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv()  # carrega .env local (no Render já vem de Environment)

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# Secret Key
app.secret_key = os.getenv("SECRET_KEY", "spero_secret_key")
app.permanent_session_lifetime = timedelta(hours=4)

# Compressão HTTP
Compress(app)

# -----------------------------------------------------------------------------
# MULTI-IDIOMA (pt/en/es) via arquivos JSON em /translations
# -----------------------------------------------------------------------------
LANG_FILES = {
    "en": os.path.join(BASE_DIR, "translations", "en.json"),
    "es": os.path.join(BASE_DIR, "translations", "es.json"),
    "pt": os.path.join(BASE_DIR, "translations", "pt.json"),
}

def load_language(lang_code: str) -> dict:
    path = LANG_FILES.get(lang_code, LANG_FILES["en"])
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.context_processor
def inject_lang():
    lang = request.args.get("lang", "en")
    t = load_language(lang)
    # helper simples: {{ t.get('home_title') }}
    return {"lang": lang, "t": t}

# -----------------------------------------------------------------------------
# E-MAIL (SendGrid/SMTP via Flask-Mail)
# -----------------------------------------------------------------------------
# Use as envs já configuradas no Render:
# MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.sendgrid.net")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", "587"))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME", "apikey")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD", os.getenv("SENDGRIP_API_KEY", ""))  # compatibilidade
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER", "contact@spero-restoration.com")

mail = Mail(app)

# -----------------------------------------------------------------------------
# UPLOAD (painel admin) — salva em /static/uploads
# -----------------------------------------------------------------------------
UPLOAD_FOLDER = os.path.join(app.static_folder, "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# -----------------------------------------------------------------------------
# PÁGINAS PÚBLICAS
# -----------------------------------------------------------------------------
@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/services")
def services_page():
    return render_template("services.html")

@app.route("/contact", methods=["GET", "POST"])
def contact_page():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        service = request.form.get("service", "").strip()
        message = request.form.get("message", "").strip()

        # e-mail vai para contact@ + cópia opcional
        to_main = os.getenv("CONTACT_TO", "contact@spero-restoration.com")
        cc_addr = os.getenv("CONTACT_CC", "roberto.maffra@gmail.com")

        try:
            msg = Message(
                subject=f"[Spero] New Contact: {name or 'Website'}",
                recipients=[to_main],
                cc=[cc_addr] if cc_addr else None,
                body=(
                    f"Name: {name}\n"
                    f"Email: {email}\n"
                    f"Phone: {phone}\n"
                    f"Service: {service}\n\n"
                    f"Message:\n{message}"
                )
            )
            mail.send(msg)
            flash("Your message was sent. We’ll contact you shortly.", "success")
            return redirect(url_for("thank_you"))
        except Exception as e:
            print(f"[Email] error: {e}")
            flash("We couldn't send your message right now. Please call us.", "danger")
            return redirect(url_for("contact_page"))

    return render_template("contact.html")

@app.route("/thank-you")
def thank_you():
    return render_template("thank-you.html")

# -----------------------------------------------------------------------------
# ADMIN — login / logout / dashboard
# -----------------------------------------------------------------------------
def is_authed() -> bool:
    return request.cookies.get("admin_auth") == "true"

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        admin_user = os.getenv("ADMIN_USER", "RobertoMaffra")
        admin_pass = os.getenv("ADMIN_PASSWORD", "SperoSecure!2025")

        if username == admin_user and password == admin_pass:
            resp = make_response(redirect(url_for("admin_dashboard")))
            # cookie de 1h, httpOnly e samesite=Lax
            resp.set_cookie("admin_auth", "true", max_age=3600, httponly=True, samesite="Lax")
            flash("Login successful!", "success")
            return resp
        else:
            error = "Invalid username or password."
            flash(error, "danger")

    return render_template("admin_login.html", error=error)

@app.route("/admin-logout")
def admin_logout():
    resp = make_response(redirect(url_for("admin_login")))
    resp.set_cookie("admin_auth", "", expires=0)
    flash("You have been logged out successfully.", "info")
    return resp

@app.route("/admin")
def admin_dashboard():
    if not is_authed():
        return redirect(url_for("admin_login"))

    # lista de uploads (somente arquivos permitidos)
    try:
        files = [
            f for f in os.listdir(UPLOAD_FOLDER)
            if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))
            and allowed_file(f)
        ]
    except Exception as e:
        print(f"[Admin] error listing uploads: {e}")
        files = []

    # URL pública para imagem: /static/uploads/<file>
    return render_template(
        "admin.html",
        uploads=files,
        ADMIN_USER=os.getenv("ADMIN_USER", "admin")
    )

# Upload via formulário do admin.html (POST)
@app.route("/upload", methods=["POST"])
def upload_file():
    if not is_authed():
        return redirect(url_for("admin_login"))

    if "file" not in request.files:
        flash("No file part", "warning")
        return redirect(url_for("admin_dashboard"))

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file", "warning")
        return redirect(url_for("admin_dashboard"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        flash("File uploaded successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    flash("Invalid file type.", "danger")
    return redirect(url_for("admin_dashboard"))

# Opcional: servir uploads direto (útil para preview em alguns ambientes)
@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# -----------------------------------------------------------------------------
# DIAGNÓSTICO
# -----------------------------------------------------------------------------
@app.route("/test-email")
def test_email():
    try:
        to_main = os.getenv("CONTACT_TO", "contact@spero-restoration.com")
        msg = Message(
            subject="[Spero] Test Email",
            recipients=[to_main],
            body="Test email from deployed app."
        )
        mail.send(msg)
        return "✅ Test email sent successfully!"
    except Exception as e:
        return f"❌ Email error: {e}"

@app.route("/healthz")
def healthz():
    return jsonify(ok=True), 200

# -----------------------------------------------------------------------------
# GUNICORN ENTRYPOINT LOCAL (Render usa gunicorn externo)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
