# ======================================================
# SPERO RESTORATION - CONTACT ROUTES
# ======================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
from config import Config
import requests
import json

contact_bp = Blueprint("contact", __name__)

# ------------------------------------------------------
# CONTACT FORM PAGE
# ------------------------------------------------------
@contact_bp.route("/contact")
def contact_page():
    meta = {
        "title": "Contact Spero Restoration | 24/7 Emergency Response",
        "description": "Get in touch with Spero Restoration for water, mold, or fire damage assistance. We offer 24/7 emergency services in Orlando.",
        "url": f"{Config.DOMAIN}/contact",
    }
    return render_template("contact.html", meta=meta)


# ------------------------------------------------------
# HANDLE FORM SUBMISSION
# ------------------------------------------------------
@contact_bp.route("/send_email", methods=["POST"])
def send_email():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    message = request.form.get("message")

    if not name or not email or not message:
        flash("Please fill out all required fields.")
        return redirect(url_for("contact.contact_page"))

    # --------------------------------------------------
    # SendGrid API Integration
    # --------------------------------------------------
    try:
        sendgrid_url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {Config.SENDGRID_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "personalizations": [
                {
                    "to": [{"email": Config.CONTACT_EMAIL}],
                    "bcc": [{"email": Config.BCC_EMAIL}],
                    "subject": f"New Contact Form Submission from {name}"
                }
            ],
            "from": {"email": Config.CONTACT_EMAIL, "name": "Spero Restoration Website"},
            "content": [
                {
                    "type": "text/html",
                    "value": f"""
                    <h2>New message from Spero Restoration website</h2>
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Phone:</strong> {phone}</p>
                    <p><strong>Message:</strong><br>{message}</p>
                    """
                }
            ]
        }

        response = requests.post(sendgrid_url, headers=headers, data=json.dumps(data))
        if response.status_code >= 200 and response.status_code < 300:
            return redirect(url_for("contact.thank_you"))
        else:
            flash("Error sending your message. Please try again later.")
            return redirect(url_for("contact.contact_page"))

    except Exception as e:
        print(f"SendGrid Error: {e}")
        flash("Internal error sending email.")
        return redirect(url_for("contact.contact_page"))


# ------------------------------------------------------
# THANK YOU PAGE
# ------------------------------------------------------
@contact_bp.route("/thank-you")
def thank_you():
    meta = {
        "title": "Thank You | Spero Restoration",
        "description": "We have received your message. Our team will contact you shortly.",
        "url": f"{Config.DOMAIN}/thank-you",
    }
    return render_template("thankyou.html", meta=meta)
