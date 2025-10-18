from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Email configuration (SendGrid)
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('SENDGRID_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = 'contact@spero-restoration.com'

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')

    msg = Message(subject=f"New Message from {name}",
                  recipients=['contact@spero-restoration.com', 'roberto.maffra@gmail.com'],
                  body=f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}")

    mail.send(msg)
    return "Message sent successfully!"

if __name__ == '__main__':
    app.run(debug=True)
