from flask import Flask, render_template, request, redirect, url_for
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_email():
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        content = f"New message from {name} ({email}):\n\n{message}"

        mail = Mail(
            from_email='contact@spero-restoration.com',
            to_emails='contact@spero-restoration.com',
            subject=f'New Contact Form Submission from {name}',
            plain_text_content=content
        )

        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(mail)

        return redirect(url_for('thankyou'))
    except Exception as e:
        print(e)
        return "Error sending email", 500

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
