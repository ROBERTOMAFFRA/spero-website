from flask import Flask, render_template, request, redirect, url_for, flash
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "spero_secret_key")

# === Home Route ===
@app.route('/')
def index():
    return render_template('index.html')

# === About Us Page ===
@app.route('/about')
def about():
    return render_template('about.html')

# === Privacy Policy Page ===
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# === Terms of Use Page ===
@app.route('/terms')
def terms():
    return render_template('terms.html')

# === Thank You Page ===
@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

# === Contact Form ===
@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not all([name, email, message]):
        flash('Please fill out all fields before submitting.', 'error')
        return redirect(url_for('index'))

    subject = f"New Contact Form Submission from {name}"
    content = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        mail = Mail(
            from_email='contact@spero-restoration.com',
            to_emails='contact@spero-restoration.com',
            subject=subject,
            plain_text_content=content
        )
        sg.send(mail)
        flash('Message sent successfully! Thank you for contacting us.', 'success')
        return redirect(url_for('thankyou'))

    except Exception as e:
        print(f"Error sending email: {e}")
        flash('There was an error sending your message. Please try again later.', 'error')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
