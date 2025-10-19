from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "contact@spero-restoration.com"
TO_EMAILS = ["contact@spero-restoration.com", "roberto.maffra@gmail.com"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        service = request.form.get("service")
        message = request.form.get("message")

        # corpo principal do e-mail
        full_message = f"""
New Inspection Request
-------------------------
Name: {name}
Email: {email}
Phone: {phone}
Service: {service}
Message: {message}
        """

        try:
            # 1️⃣ Envia e-mail para equipe Spero
            for recipient in TO_EMAILS:
                requests.post(
                    "https://api.sendgrid.com/v3/mail/send",
                    headers={
                        "Authorization": f"Bearer {SENDGRID_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "personalizations": [{"to": [{"email": recipient}]}],
                        "from": {"email": FROM_EMAIL, "name": "Spero Restoration"},
                        "subject": f"New Inspection Request from {name}",
                        "content": [{"type": "text/plain", "value": full_message}],
                    },
                )

            # 2️⃣ Envia confirmação automática para o cliente
            confirm_msg = f"""
Hi {name},

Thank you for contacting Spero Restoration.
We received your request regarding: {service}.
Our team will get in touch with you shortly at {phone}.

Best regards,
Spero Restoration Team
(407) 724-6310
contact@spero-restoration.com
            """

            requests.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={
                    "Authorization": f"Bearer {SENDGRID_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "personalizations": [{"to": [{"email": email}]}],
                    "from": {"email": FROM_EMAIL, "name": "Spero Restoration"},
                    "subject": "We received your request — Spero Restoration",
                    "content": [{"type": "text/plain", "value": confirm_msg}],
                },
            )

            return render_template("contact.html", success=True)

        except Exception as e:
            print("Error sending email:", e)
            return render_template("contact.html", error=True)

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
