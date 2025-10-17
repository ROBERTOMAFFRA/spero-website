from flask import Flask, render_template, request, jsonify
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_email():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        content = f"""
        New inspection request from Spero Restoration website:

        Name: {name}
        Email: {email}
        Phone: {phone}
        Message:
        {message}
        """

        msg = Mail(
            from_email='contact@spero-restoration.com',
            to_emails=['contact@spero-restoration.com', 'roberto.maffra@gmail.com'],
            subject='New Inspection Request – Spero Restoration',
            plain_text_content=content
        )

        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        sg.send(msg)

        return jsonify({'success': True, 'message': 'Your request has been sent successfully.'})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': 'Something went wrong. Please try again later.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

