from flask import Flask, render_template, request, redirect, url_for
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

# Rota principal
@app.route('/')
def home():
    return render_template('index.html')

# Rota de envio do formulário
@app.route('/send', methods=['POST'])
def send_email():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')

    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    to_email_1 = os.getenv('TO_EMAIL_1', 'contact@spero-restoration.com')
    to_email_2 = os.getenv('TO_EMAIL_2', 'roberto.maffra@gmail.com')

    if not sendgrid_api_key:
        return "Error: SendGrid API Key not found."

    # Monta o conteúdo do e-mail
    email_content = f"""
    New message from Spero Restoration website:
    
    Name: {name}
    Email: {email}
    Phone: {phone}
    Message: {message}
    """

    message_obj = Mail(
        from_email='contact@spero-restoration.com',
        to_emails=[to_email_1, to_email_2],
        subject='New Contact Form Submission - Spero Restoration',
        plain_text_content=email_content
    )

    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        sg.send(message_obj)
        return redirect(url_for('thank_you'))
    except Exception as e:
        print(f"Error sending email: {e}")
        return "There was an issue sending your message."

@app.route('/thank-you')
def thank_you():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)
