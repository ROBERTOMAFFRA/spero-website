from flask import Flask, render_template, request, jsonify
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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
        address = request.form.get('address')
        message = request.form.get('message')

        subject = f"New Inspection Request from {name}"
        body = f"""
        Name: {name}
        Email: {email}
        Phone: {phone}
        Address: {address}
        Message:
        {message}
        """

        msg = Mail(
            from_email=os.environ.get('MAIL_DEFAULT_SENDER'),
            to_emails=[
                'contact@spero-restoration.com',
                'roberto.maffra@gmail.com'
            ],
            subject=subject,
            plain_text_content=body
        )

        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(msg)

        return jsonify(success=True, message="Message sent successfully!")
    except Exception as e:
        print("Error:", e)
        return jsonify(success=False, message="Error sending message.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
