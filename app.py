from flask import Flask, render_template, request, redirect, flash
import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

app = Flask(__name__)
app.secret_key = "spero_secret_key"

# Carrega a chave do SendGrid do Render
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "contact@spero-restoration.com"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_email", methods=["POST"])
def send_email():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

    html_content = f"""
    <h2>New message from Spero Restoration Website</h2>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Message:</strong><br>{message}</p>
    """

    mail = Mail(
        from_email=Email(FROM_EMAIL),
        to_emails=[
            To("contact@spero-restoration.com"),
            To("roberto.maffra@gmail.com")
        ],
        subject="New Contact Form Submission - Spero Restoration",
        html_content=Content("text/html", html_content)
    )

    try:
        sg.send(mail)
        flash("✅ Message sent successfully! We'll get back to you soon.", "success")
    except Exception as e:
        flash("❌ Error sending message. Please try again later.", "error")
        print("SendGrid Error:", str(e))

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
