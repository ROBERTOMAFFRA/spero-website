from flask import Flask, render_template, request, redirect
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        sg = SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))

        # Email principal para você
        msg = Mail(
            from_email='contact@spero-restoration.com',
            to_emails='contact@spero-restoration.com',
            subject=f'New message from {name}',
            plain_text_content=f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}'
        )
        sg.send(msg)

        # Auto resposta ao cliente
        auto = Mail(
            from_email='contact@spero-restoration.com',
            to_emails=email,
            subject='We received your message!',
            plain_text_content=f'Hi {name},\n\nThanks for contacting Spero Restoration. Our team will get back to you soon.\n\n— Spero Restoration Team'
        )
        sg.send(auto)

        return redirect('/thankyou')

    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return "Email sending failed.", 500


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
