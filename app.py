from flask import Flask, render_template, request, redirect, url_for
import os
import requests

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Send email using SendGrid
@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')

    subject = f"New Inspection Request from {name}"
    content = f"""
    🏠 New Inspection Request:

    Name: {name}
    Email: {email}
    Phone: {phone}

    Message:
    {message}

    -------------------------------------
    Sent automatically from Spero Restoration Website.
    """

    # SendGrid API
    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
    if not sendgrid_api_key:
        return "SendGrid API Key not found. Please configure it in Render environment variables.", 500

    data = {
        "personalizations": [
            {
                "to": [
                    {"email": "contact@spero-restoration.com"},
                    {"email": "roberto.maffra@gmail.com"}
                ],
                "subject": subject
            }
        ],
        "from": {"email": "contact@spero-restoration.com"},
        "content": [
            {"type": "text/plain", "value": content}
        ]
    }

    try:
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {sendgrid_api_key}",
                "Content-Type": "application/json"
            },
            json=data
        )

        if response.status_code in [200, 202]:
            print("✅ Email sent successfully")
        else:
            print("⚠️ SendGrid response:", response.status_code, response.text)

    except Exception as e:
        print("❌ Error sending email:", e)
        return "An error occurred while sending email.", 500

    # Confirmation page
    return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return """
    <html>
      <head><meta http-equiv='refresh' content='3;url=/' /></head>
      <body style='font-family:Arial; text-align:center; padding-top:50px;'>
        <h2>✅ Your request has been received!</h2>
        <p>We’ll contact you as soon as possible to schedule your inspection.</p>
        <p>Redirecting back to homepage...</p>
      </body>
    </html>
    """

# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
