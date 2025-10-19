from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        service = request.form["service"]
        message = request.form["message"]
        photo_before = request.files.get("photo_before")
        photo_after = request.files.get("photo_after")

        try:
            msg = EmailMessage()
            msg["Subject"] = f"New Inspection Request from {name}"
            msg["From"] = "contact@spero-restoration.com"
            msg["To"] = ["contact@spero-restoration.com", "roberto.maffra@gmail.com"]
            msg.set_content(f"""
Name: {name}
Email: {email}
Phone: {phone}
Service: {service}
Message: {message}
            """)

            # Attach photos if provided
            for photo in [photo_before, photo_after]:
                if photo and photo.filename:
                    msg.add_attachment(photo.read(), maintype="image", subtype="jpeg", filename=photo.filename)

            # Send email
            with smtplib.SMTP("smtp.zoho.com", 587) as smtp:
                smtp.starttls()
                smtp.login("contact@spero-restoration.com", "YOUR_ZOHO_PASSWORD")
                smtp.send_message(msg)

            # Confirmation email for client
            confirm = EmailMessage()
            confirm["Subject"] = "We received your request — Spero Restoration"
            confirm["From"] = "contact@spero-restoration.com"
            confirm["To"] = email
            confirm.set_content(f"""
Hi {name},

Thank you for contacting Spero Restoration.
We received your request about: {service}.
Our team will contact you shortly at {phone}.

Best regards,
Spero Restoration Team
            """)

            with smtplib.SMTP("smtp.zoho.com", 587) as smtp:
                smtp.starttls()
                smtp.login("contact@spero-restoration.com", "YOUR_ZOHO_PASSWORD")
                smtp.send_message(confirm)

            return render_template("contact.html", success=True)
        except Exception as e:
            print("Error:", e)
            return render_template("contact.html", error=True)

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
