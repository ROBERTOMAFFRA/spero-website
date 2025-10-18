from flask import Flask, render_template, request, redirect, url_for
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    phone = request.form.get('phone', '')
    service = request.form.get('service', '')
    message = request.form['message']

    content = f"""
    New message from Spero Restoration website:

    Name: {name}
    Email: {email}
    Phone: {phone}
    Service: {service}
    Message:
    {message}
    """

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        mail = Mail(
            from_email='contact@spero-restoration.com',
            to_emails='contact@spero-restoration.com',
            subject=f'New Lead from {name}',
            plain_text_content=content
        )
        sg.send(mail)
    except Exception as e:
        print(e)

    return redirect(url_for('thank_you'))

if __name__ == '__main__':
    app.run(debug=True)
