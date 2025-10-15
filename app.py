from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "spero_secret")

# ========= HOME PAGE =========
@app.route("/")
def home():
    return render_template("index.html")

# ========= ABOUT =========
@app.route("/about")
def about():
    return render_template("about.html")

# ========= PRIVACY =========
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

# ========= TERMS =========
@app.route("/terms")
def terms():
    return render_template("terms.html")

# ========= CONTACT / LEADS =========
@app.route("/send_email", methods=["POST"])
def send_email():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not name or not email or not message:
        flash("All fields are required.", "error")
        return redirect(url_for("home"))

    subject = f"New Lead from {name}"
    content = f"""
    Name: {name}
    Email: {email}
    Message: {message}
    """

    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
    sender_email = os.getenv("SENDER_EMAIL", "contact@spero-restoration.com")
    recipient_email = os.getenv("RECIPIENT_EMAIL", "contact@spero-restoration.com")

    if sendgrid_api_key:
        try:
            response = requests.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={
                    "Authorization": f"Bearer {sendgrid_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "personalizations": [{"to": [{"email": recipient_email}]}],
                    "from": {"email": sender_email},
                    "subject": subject,
                    "content": [{"type": "text/plain", "value": content}]
                }
            )

            if response.status_code == 202:
                flash("Message sent successfully!", "success")
            else:
                flash(f"Error sending email: {response.text}", "error")

        except Exception as e:
            flash(f"Exception: {e}", "error")
    else:
        flash("Email service not configured. Please set SENDGRID_API_KEY.", "error")

    return redirect(url_for("thankyou"))

# ========= THANK YOU PAGE =========
@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

if __name__ == "__main__":
    app.run(debug=True)
