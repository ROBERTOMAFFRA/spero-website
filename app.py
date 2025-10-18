from flask import Flask, render_template, request, redirect, url_for
import os, sendgrid
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

# --- Load Translations ---
import json
def load_translation(lang):
    try:
        with open(f"translations/{lang}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        with open("translations/en.json", "r", encoding="utf-8") as f:
            return json.load(f)

# --- Routes ---
@app.route("/")
def home():
    lang = request.args.get("lang", "en")
    t = load_translation(lang)
    return render_template("index.html", lang=lang, t=t)

@app.route("/about")
def about():
    lang = request.args.get("lang", "en")
    t = load_translation(lang)
    return render_template("about.html", lang=lang, t=t)

@app.route("/services")
def services():
    lang = request.args.get("lang", "en")
    t = load_translation(lang)
    return render_template("services.html", lang=lang, t=t)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    lang = request.args.get("lang", "en")
    t = load_translation(lang)
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        service = request.form["service"]
        message = request.form["message"]

        sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
        content = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nService: {service}\nMessage: {message}"

        email_to_send = Mail(
            from_email="contact@spero-restoration.com",
            to_emails=["contact@spero-restoration.com", "roberto.maffra@gmail.com"],
            subject=f"New Contact Request from {name}",
            plain_text_content=content
        )
        sg.send(email_to_send)
        return redirect(url_for("thank_you", lang=lang))
    return render_template("contact.html", lang=lang, t=t)

@app.route("/thank-you")
def thank_you():
    lang = request.args.get("lang", "en")
    t = load_translation(lang)
    return render_template("thank-you.html", lang=lang, t=t)

@app.route("/privacy")
def privacy():
    lang = request.args.get("lang", "en")
    t = load_translation(lang)
    return render_template("privacy.html", lang=lang, t=t)

@app.route("/terms")
def terms():
    lang = request.args.get("lang", "en")
    t = load_translation(lang)
    return render_template("terms.html", lang=lang, t=t)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
