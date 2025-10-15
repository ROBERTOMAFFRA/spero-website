from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import time   # ✅ Adicionado
import pytz   # ✅ Adicionado
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# =============================
# TIMEZONE CONFIG (Orlando / Eastern Time)
# =============================
os.environ['TZ'] = 'America/New_York'  # ✅ Fixa o fuso horário no servidor
time.tzset()  # ✅ Aplica o fuso no ambiente

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

    # Captura o horário atual no fuso de Orlando
    tz = pytz.timezone("America/New_York")
    local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    subject = f"New Lead from {name}"
    body = f"""
You received a new message from the Spero Restoration website:

Name: {name}
Email: {email}

Message:
{message}

Time received (Eastern Time): {local_time}
"""

    recipients = [
        "contact@spero-restoration.com",
        "roberto.maffra@gmail.com"
    ]

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        for to_email in recipients:
            mail = Mail(
                from_email="contact@spero-restoration.com",
                to_emails=to_email,
                subject=subject,
                plain_text_content=body
            )
            sg.send(mail)
        print("✅ Email sent successfully to both recipients.")
        return redirect(url_for('thank_you'))
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return f"Error sending email: {str(e)}", 500

# =============================
# THANK YOU PAGE
# =============================
@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

# =============================
# SEO FILES
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
