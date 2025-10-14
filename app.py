from flask import Flask, render_template, request, redirect, url_for
import os
import requests

app = Flask(__name__)

# Página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Página sobre
@app.route('/about')
def about():
    return render_template('about.html')

# Política de privacidade
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# Termos de uso
@app.route('/terms')
def terms():
    return render_template('terms.html')

# Página de agradecimento
@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

# Envio do formulário via SendGrid
@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
    if not sendgrid_api_key:
        return "SendGrid API key not found.", 500

    data = {
        "personalizations": [{
            "to": [{"email": "contact@spero-restoration.com"}],
            "cc": [{"email": "roberto.maffra@gmail.com"}],
            "subject": f"New contact from {name}"
        }],
        "from": {"email": "contact@spero-restoration.com"},
        "content": [{
            "type": "text/plain",
            "value": f"Name: {name}\nEmail: {email}\nMessage: {message}"
        }]
    }

    response = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={"Authorization": f"Bearer {sendgrid_api_key}", "Content-Type": "application/json"},
        json=data
    )

    if response.status_code == 202:
        return redirect(url_for('thankyou'))
    else:
        return f"Email sending failed: {response.text}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
