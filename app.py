from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

# =============================
# HOME ROUTE
# =============================
@app.route('/')
def home():
    return render_template('index.html')


# =============================
# EMAIL ROUTE (SendGrid)
# =============================
@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not all([name, email, message]):
        return "All fields are required.", 400

    subject = f"New Contact from {name}"
    body = f"""
You received a new message from the Spero Restoration website:

Name: {name}
Email: {email}

Message:
{message}
"""

    # Destinatários principais
    recipients = [
        "contact@spero-restoration.com",
        "roberto.maffra@gmail.com"
    ]

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        mail = Mail(
            from_email="contact@spero-restoration.com",  # remetente autenticado
            to_emails=recipients,
            subject=subject,
            plain_text_content=body
        )

        response = sg.send(mail)
        print(f"✅ Email sent successfully. Status Code: {response.status_code}")
        return redirect(url_for('thank_you'))

    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return render_template('email_error.html', error=str(e)), 500


# =============================
# THANK YOU PAGE
# =============================
@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')


# =============================
# SEO FILES (robots.txt & sitemap.xml)
# =============================
@app.route('/robots.txt')
def robots():
    return send_from_directory('.', 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')


# =============================
# RUN LOCAL
# =============================
if __name__ == '__main__':
    app.run(debug=True)
