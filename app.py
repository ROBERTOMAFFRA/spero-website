import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_compress import Compress
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from flask_mail import Mail, Message

# =======================================
# CONFIGURAÇÕES BÁSICAS
# =======================================
load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY", "spero_secret_key")
Compress(app)

# =======================================
# SUPORTE MULTI-IDIOMA
# =======================================
LANG_FILES = {
    "en": "static/lang/en.json",
    "es": "static/lang/es.json",
    "pt": "static/lang/pt.json"
}

def load_language(lang_code):
    try:
        with open(LANG_FILES.get(lang_code, LANG_FILES["en"]), encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.context_processor
def inject_lang():
    lang = request.args.get("lang", "en")
    return {"lang": lang, "t": load_language(lang)}

# =======================================
# ROTA PÚBLICA (HOME)
# =======================================
@app.route("/")
def index():
    return render_template("index.html")

# =======================================
# CONTATO / SOBRE / PÁGINAS ESTÁTICAS
# =======================================
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# =======================================
# CONFIGURAÇÃO DE E-MAIL (SENDGRID)
# =======================================
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.sendgrid.net")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME", "apikey")
app.config["MAIL_PASSWORD"] = os.getenv("SENDGRID_API_KEY", "")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER", "contact@spero-restoration.com")

mail = Mail(app)

@app.route("/test-email")
def test_email():
    try:
        msg = Message(
            "Test Email from Spero Restoration",
            recipients=["contact@spero-restoration.com"],
            body="This is a test email from your deployed Render app."
        )
        mail.send(msg)
        return "✅ Test email sent successfully!"
    except Exception as e:
        print(f"Email error: {e}")
        return f"❌ Error sending email: {e}"

# =======================================
# SISTEMA DE LOGIN ADMIN
# =======================================
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin_user = os.getenv("ADMIN_USER", "RobertoMaffra")
        admin_pass = os.getenv("ADMIN_PASSWORD", "SperoSecure!2025")

        if username == admin_user and password == admin_pass:
            resp = make_response(redirect(url_for("admin_dashboard")))
            resp.set_cookie("admin_auth", "true", max_age=3600, httponly=True, samesite="Lax")
            flash("✅ Login successful! Welcome to admin dashboard.", "success")
            return resp
        else:
            flash("❌ Invalid username or password.", "danger")
            error = "Invalid credentials."

    return render_template("admin_login.html", error=error)

# =======================================
# ADMIN LOGOUT
# =======================================
@app.route("/admin-logout")
def admin_logout():
    resp = make_response(redirect(url_for("admin_login")))
    resp.set_cookie("admin_auth", "", expires=0)
    flash("You have been logged out successfully.", "info")
    return resp

# =======================================
# ADMIN DASHBOARD
# =======================================
@app.route("/admin")
def admin_dashboard():
    try:
        auth = request.cookies.get("admin_auth")
        if auth != "true":
            return redirect(url_for("admin_login"))

        upload_folder = os.path.join(app.static_folder, "uploads")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        uploads = [f for f in os.listdir(upload_folder) if not f.startswith(".")]
        return render_template("admin.html", uploads=uploads, ADMIN_USER=os.getenv("ADMIN_USER"))
    except Exception as e:
        print(f"⚠️ Error in admin_dashboard: {e}")
        flash("Error loading dashboard.", "error")
        return redirect(url_for("index"))

# =======================================
# UPLOAD DE IMAGENS (PAINEL ADMIN)
# =======================================
@app.route("/upload", methods=["POST"])
def upload_file():
    auth = request.cookies.get("admin_auth")
    if auth != "true":
        return redirect(url_for("admin_login"))

    if "file" not in request.files:
        flash("No file part", "warning")
        return redirect(url_for("admin_dashboard"))

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file", "warning")
        return redirect(url_for("admin_dashboard"))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.static_folder, "uploads", filename)
    file.save(filepath)
    flash("✅ File uploaded successfully", "success")
    return redirect(url_for("admin_dashboard"))

# =======================================
# EXECUÇÃO DO APP
# =======================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
