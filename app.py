from flask import Flask, render_template, request, redirect, url_for, flash
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "spero_secret_key")

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Email send route
@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        name = request.form['name']
        email = request.form['email']
        phone = request.form.get('phone', 'Not provided')
        message = request.form['message']

        content = f"""
        🧾 New Inspection Request from Spero Website
        ---------------------------------------
        Name: {name}
        Email: {email}
        Phone: {phone}

        Message:
        {message}
        """

        # SendGrid setup
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        from_email = os.getenv('FROM_EMAIL', 'contact@spero-restoration.com')
        to_emails = [
            'contact@spero-restoration.com',
            'roberto.maffra@gmail.com'
        ]

        mail = Mail(
            from_email=from_email,
            to_emails=to_emails,
            subject='🛠️ New Inspection Request - Spero Restoration',
            plain_text_content=content
        )

        sg.send(mail)
        flash('✅ Your request has been sent successfully! We’ll contact you soon.', 'success')

    except Exception as e:
        print(f"Error sending email: {e}")
        flash('⚠️ Something went wrong. Please try again later.', 'error')

    return redirect(url_for('home'))

# Privacy and Terms (optional)
@app.route('/privacy')
def privacy():
    return "<h2>Privacy Policy</h2><p>Your information is kept confidential and only used for communication related to our services.</p>"

@app.route('/terms')
def terms():
    return "<h2>Terms of Use</h2><p>By using this site, you agree to our service terms and conditions.</p>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
