from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os
import smtplib

app = Flask(__name__)

# ---- Zoho Mail Configuration ----
app.config['MAIL_SERVER'] = 'smtp.zoho.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send_email():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    msg = Message(
        subject=f"New message from {name}",
        sender=app.config['MAIL_USERNAME'],
        recipients=['contact@spero-restoration.com', 'roberto.maffra@gmail.com'],
        body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    )

    try:
        print("🔧 Connecting to Zoho SMTP server...")
        with mail.connect() as conn:
            # habilita log detalhado SMTP
            conn.connection.set_debuglevel(1)
            conn.connection.timeout = 15
            conn.send(msg)
        print("✅ Email successfully sent!")
        return "Message sent successfully!"
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication error: {e}")
        return "Authentication failed — please check username or app password."
    except smtplib.SMTPConnectError as e:
        print(f"❌ Connection error: {e}")
        return "Connection failed — please check Zoho SMTP settings."
    except Exception as e:
        print(f"⚠️ General error: {e}")
        return f"Error sending message: {e}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
