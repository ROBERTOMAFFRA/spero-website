from flask import Flask, render_template, request, redirect, url_for
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

@app.route('/')
def home():
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

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    sendgrid_api = os.getenv('SENDGRID_API_KEY')
    if not sendgrid_api:
        return "SendGrid API Key not configured", 500

    content = f"""
    New message from {name} ({email}):
    {message}
    """

    message = Mail(
        from_email='contact@spero-restoration.com',
        to_emails=['contact@spero-restoration.com', 'roberto.maffra@gmail.com'],
        subject='New Contact Form Submission - Spero Restoration',
        plain_text_content=content
    )

    try:
        sg = SendGridAPIClient(sendgrid_api)
        sg.send(message)
        return redirect(url_for('thankyou'))
    except Exception as e:
        print(e)
        return "Error sending email", 500

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == "__main__":
    app.run(debug=False)
