from flask import Flask, render_template, request, redirect, url_for, flash
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "spero_secret_key")

# Página principal
@app.route("/")
def home():
    return render_template("index.html")

# Formulário de agendamento
@app.route("/send_email", methods=["POST"])
def send_email():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    message = request.form.get("message", "No additional message provided")

    subject = f"New Inspection Request from {name}"
    content = f"""
    <strong>Inspection Request Details:</strong><br>
    <b>Name:</b> {name}<br>
    <b>Email:</b> {email}<br>
    <b>Phone:</b> {phone}<br>
    <b>Message:</b><br>{message}<br><br>
    ⚡ Sent from Spero Restoration website.
    """

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        email_msg = Mail(
            from_email="contact@spero-restoration.com",
            to_emails=["contact@spero-restoration.com", "roberto.maffra@gmail.com"],
            subject=subject,
            html_content=content
        )
        sg.send(email_msg)
        flash("✅ Your request was successfully sent. We'll contact you soon.", "success")
    except Exception as e:
        flash("❌ There was an issue sending your request. Please try again later.", "danger")
        print(f"SendGrid Error: {e}")

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
