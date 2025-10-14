from flask import Flask, render_template, request, redirect, url_for
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

# Load environment variables
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "contact@spero-restoration.com"
TO_EMAIL = "contact@spero-restoration.com"
CC_EMAIL = "roberto.maffra@gmail.com"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not SENDGRID_API_KEY:
        return "SendGrid API key not configured", 500

    subject = f"New Lead from {name}"
    body = f"""
    Name: {name}
    Email: {email}
    Message:
    {message}
    """

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        mail = Mail(
            from_email=FROM_EMAIL,
            to_emails=[TO_EMAIL, CC_EMAIL],
            subject=subject,
            plain_text_content=body
        )
        sg.send(mail)
        return redirect(url_for('thankyou'))
    except Exception as e:
        print(f"Error sending email: {e}")
        return "Error sending email", 500


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
