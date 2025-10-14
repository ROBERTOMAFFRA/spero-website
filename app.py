from flask import Flask, render_template, request, redirect, url_for
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    content = f"New message from {name} ({email}):\n\n{message}"

    to_email = os.environ.get('TO_EMAIL')
    cc_email = os.environ.get('CC_EMAIL')
    from_email = os.environ.get('FROM_EMAIL')

    mail = Mail(
        from_email=from_email,
        to_emails=[to_email, cc_email],
        subject="New Contact Form Message - Spero Restoration",
        plain_text_content=content
    )

    try:
        sg.send(mail)
        return redirect(url_for('thankyou'))
    except Exception as e:
        print(e)
        return "An error occurred while sending the message."

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
