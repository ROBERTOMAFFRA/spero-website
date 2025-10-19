import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_compress import Compress
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json

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
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
