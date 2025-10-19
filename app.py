# ======================================================
# Spero Restoration Corp — Flask App
# Revisão completa de imports (SEO, Email, Multi-idioma, Uploads)
# ======================================================

from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, send_from_directory, jsonify
)
from flask_mail import Mail, Message
from flask_compress import Compress
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail as SendGridMail
from dotenv import load_dotenv
import os
import json
import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "spero_secret_key")
Compress(app)

# ---------------------------
# MULTI-LANGUAGE SUPPORT
# ---------------------------
LANG_FILES = {
    "en": "static/lang/en.json",
    "es": "static/lang/es.json",
    "pt": "static/lang/pt.json"
}

def load_language(lang_code):
    path = LANG_FILES.get(lang_code, LANG_FILES["en"])
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.context_processor
def inject_lang():
    lang = request.args.get("lang", "en")
    return {"lang": lang, "t": load_language(lang)}

# ---------------------------
# ROUTES
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        try:
            send_email(name, email, phone, message)
            flash("success")
            return render_template("contact.html", success=True)
        except Exception as e:
            print("Error sending email:", e)
            flash("error")
            return render_template("contact.html", success=False)
    return render_template("contact.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

# ---------------------------
# EMAIL HANDLER (SENDGRID)
# ---------------------------
def send_email(name, email, phone, message):
    sg_api = os.getenv("SENDGRID_API_KEY")
    if not sg_api:
        raise ValueError("SENDGRID_API_KEY missing in environment")

    subject = f"New Contact Form Submission from {name}"
    content = f"""
    Name: {name}
    Email: {email}
    Phone: {phone}
    Message:
    {message}
    """

    mail = Mail(
        from_email="contact@spero-restoration.com",
        to_emails=["contact@spero-restoration.com", "roberto.maffra@gmail.com"],
        subject=subject,
        plain_text_content=content
    )

    sg = SendGridAPIClient(sg_api)
    sg.send(mail)

# ---------------------------
# SITEMAP & ROBOTS
# ---------------------------
@app.route("/sitemap.xml")
def sitemap():
    pages = [
        {"loc": url_for("index", _external=True)},
        {"loc": url_for("about", _external=True)},
        {"loc": url_for("services", _external=True)},
        {"loc": url_for("contact", _external=True)},
        {"loc": url_for("privacy", _external=True)},
        {"loc": url_for("terms", _external=True)},
    ]
    xml = render_template("sitemap.xml", pages=pages)
    return app.response_class(xml, mimetype="application/xml")

@app.route("/robots.txt")
def robots():
    return app.send_static_file("robots.txt")

# ---------------------------
# CACHE CONTROL
# ---------------------------
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "public, max-age=3600"
    return response

# ---------------------------
# RUN
# ---------------------------

from werkzeug.utils import secure_filename

# ---------------------------
# ADMIN PANEL CONFIG
# ---------------------------
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ADMIN_USER = os.getenv("ADMIN_USER", "RobertoMaffra")
ADMIN_PASS = os.getenv("ADMIN_PASS", "Spero123!")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------------------
# ADMIN LOGIN
# ---------------------------
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USER and password == ADMIN_PASS:
            # Create simple session flag
            response = redirect(url_for("admin_dashboard"))
            response.set_cookie("admin_auth", "true", max_age=3600)
            return response
        else:
            flash("Invalid credentials", "error")
    return render_template("admin-login.html")

# ---------------------------
# ADMIN DASHBOARD
# ---------------------------
@app.route("/admin-dashboard")
def admin_dashboard():
    auth = request.cookies.get("admin_auth")
    if auth != "true":
        return redirect(url_for("admin_login"))

    uploads = os.listdir(app.config["UPLOAD_FOLDER"])
    uploads = [f for f in uploads if allowed_file(f)]
    return render_template("admin.html", uploads=uploads)

# ---------------------------
# UPLOAD IMAGE
# ---------------------------
@app.route("/upload", methods=["POST"])
def upload_file():
    auth = request.cookies.get("admin_auth")
    if auth != "true":
        return redirect(url_for("admin_login"))

    if "file" not in request.files:
        flash("No file part")
        return redirect(url_for("admin_dashboard"))

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("admin_dashboard"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        flash("File uploaded successfully")
    return redirect(url_for("admin_dashboard"))

# ======================================================
# CONFIGURAÇÃO DE E-MAIL E SENDGRID
# ======================================================
from flask_mail import Mail, Message

# Configuração do servidor de e-mail
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", "smtp.sendgrid.net")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME", "apikey")
app.config['MAIL_PASSWORD'] = os.getenv("SENDGRID_API_KEY", "")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER", "contact@spero-restoration.com")

mail = Mail(app)
compress = Compress(app)

# ======================================================
# ROTA DE TESTE DE E-MAIL
# ======================================================
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

# ======================================================
# ADMIN DASHBOARD (GALERIA + UPLOADS)
# ======================================================
@app.route('/admin')
def admin_dashboard():
    try:
        upload_folder = os.path.join(app.static_folder, 'uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        uploads = os.listdir(upload_folder)
        uploads = [f for f in uploads if not f.startswith('.')]
        return render_template("admin.html", uploads=uploads, ADMIN_USER=os.getenv("ADMIN_USER"))
    except Exception as e:
        print(f"Error in admin_dashboard: {e}")
        flash("Error loading dashboard.", "error")
        return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded images in admin gallery"""
    return send_from_directory(os.path.join(app.static_folder, 'uploads'), filename)

# ======================================================
# ADMIN LOGIN SYSTEM
# ======================================================
from flask import make_response

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Variáveis de ambiente configuradas no Render
        admin_user = os.getenv("ADMIN_USER", "RobertoMaffra")
        admin_pass = os.getenv("ADMIN_PASSWORD", "SperoSecure!2025")

        if username == admin_user and password == admin_pass:
            resp = make_response(redirect(url_for("admin_dashboard")))
            resp.set_cookie("admin_auth", "true", max_age=3600, httponly=True, samesite="Lax")
            flash("✅ Login successful! Welcome to admin dashboard.", "success")
            return resp
        else:
            flash("❌ Invalid username or password.", "danger")

    return render_template("admin_login.html", error=error)


@app.route("/admin-logout")
def admin_logout():
    resp = make_response(redirect(url_for("admin_login")))
    resp.set_cookie("admin_auth", "", expires=0)
    flash("You have been logged out successfully.", "info")
    return resp

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
