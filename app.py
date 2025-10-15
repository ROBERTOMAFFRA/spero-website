from flask import Flask, render_template, request, redirect, url_for
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send_email", methods=["POST"])
def send_email():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not all([name, email, message]):
        return "All fields are required.", 400

    subject = f"New Lead from {name}"
    body = f"""
    You received a new message from Spero Restoration website:

    Name: {name}
    Email: {email}
    Message:
    {message}
    """

    recipients = ["contact@spero-restoration.com", "roberto.maffra@gmail.com"]

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        for to_email in recipients:
            mail = Mail(
                from_email="contact@spero-restoration.com",
                to_emails=to_email,
                subject=subject,
                plain_text_content=body
            )
            sg.send(mail)
        return redirect(url_for("thank_you"))
    except Exception as e:
        print(str(e))
        return f"Error sending email: {str(e)}", 500

@app.route("/thank-you")
def thank_you():
    return render_template("thankyou.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

if __name__ == "__main__":
    app.run(debug=True)
