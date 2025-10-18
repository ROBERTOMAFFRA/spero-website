# ==========================================
# Spero Restoration - Web Application
# ==========================================

from flask import Flask, render_template, request, redirect, url_for
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

# ================================
# ROUTES
# ================================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')


@app.route('/terms-of-service')
def terms_of_service():
    return render_template('terms-of-service.html')


@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')


# ================================
# EMAIL FUNCTION (SendGrid)
# ================================

@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    location = request.form.get('location')
    message = request.form.get('message')

    # ✅ Email content
    subject = f"New Inspection Request from {name}"
    content = f"""
    🏠 New Inspection Request Submitted
    
    Name: {name}
    Email: {email}
    Phone: {phone}
    Location: {location}

    Message:
    {message}

    ---
    Sent from Spero Restoration website
    """

    # ✅ SendGrid integration
    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        email_message = Mail(
            from_email='contact@spero-restoration.com',
            to_emails=['contact@spero-restoration.com', 'roberto.maffra@gmail.com'],
            subject=subject,
            plain_text_content=content
        )
        sendgrid_client.send(email_message)
        print("✅ Email sent successfully.")
        return redirect(url_for('thank_you'))

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return "Error sending message. Please try again later."


# ================================
# RUN APP
# ================================
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
