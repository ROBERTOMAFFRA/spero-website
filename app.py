from flask import Flask, render_template, request, redirect
import os
import sendgrid
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

# SendGrid API Key (configure in Render → Environment)
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
TO_EMAIL = "contact@spero-restoration.com"  # destination email

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

    # Email for Spero Restoration
    content = f"New message from {name} ({email}):\n\n{message}"
    mail = Mail(
        from_email=email,
        to_emails=TO_EMAIL,
        subject=f"Website Contact: {name}",
        plain_text_content=content
    )
    sg.send(mail)

    # Auto-reply
    reply = Mail(
        from_email=TO_EMAIL,
        to_emails=email,
        subject="Thank you for contacting Spero Restoration",
        plain_text_content=f"Hello {name},\n\nThank you for contacting Spero Restoration. We’ve received your message and will respond shortly.\n\n— Spero Restoration Team"
    )
    sg.send(reply)

    return redirect('/thankyou')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
