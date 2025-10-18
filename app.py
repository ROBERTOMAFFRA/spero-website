from flask import Flask, render_template, request, redirect, url_for
import os
import sendgrid
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

# ===========================
# ROUTES
# ===========================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/thank-you")
def thank_you():
    return render_template("thank-you.html")

# ===========================
# CONTACT FORM (SendGrid)
# ===========================
@app.route("/send_email", methods=["POST"])
def send_email():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    service = request.form.get("service")
    message = request.form.get("message")

    sg_api_key = os.getenv("SENDGRID_API_KEY")

    if not sg_api_key:
        print("⚠️ Missing SENDGRID_API_KEY — skipping email send.")
        return redirect(url_for("thank_you"))

    sg = sendgrid.SendGridAPIClient(api_key=sg_api_key)
    content = f"""
    Name: {name}
    Email: {email}
    Phone: {phone}
    Service: {service}
    Message: {message}
    """

    mail = Mail(
        from_email="contact@spero-restoration.com",
        to_emails="contact@spero-restoration.com",
        subject=f"New Lead from {name}",
        plain_text_content=content,
    )

    try:
        sg.send(mail)
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ SendGrid error: {e}")

    return redirect(url_for("thank_you"))

# ===========================
# 404 PAGE
# ===========================
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

# ===========================
# LOCAL EXECUTION
# ===========================
if __name__ == "__main__":
    app.run(debug=True)
