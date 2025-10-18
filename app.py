from flask import Flask, render_template, request, redirect, url_for
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        description = request.form.get("description")

        message = Mail(
            from_email=os.getenv("MAIL_DEFAULT_SENDER"),
            to_emails="contact@spero-restoration.com",
            subject=f"New Inspection Request from {name}",
            html_content=f"""
            <h2>New Inspection Request</h2>
            <p><b>Name:</b> {name}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Phone:</b> {phone}</p>
            <p><b>Description:</b> {description}</p>
            """
        )
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)

        return redirect(url_for("index", success="true"))
    except Exception as e:
        print(f"Error sending email: {e}")
        return redirect(url_for("index", success="false"))

@app.route("/privacy-policy")
def privacy():
    return render_template("privacy-policy.html")

@app.route("/terms-of-service")
def terms():
    return render_template("terms-of-service.html")

@app.route("/about-us")
def about():
    return render_template("about-us.html")

@app.route("/robots.txt")
def robots():
    return app.send_static_file("robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return app.send_static_file("sitemap.xml")

@app.before_request
def redirect_www():
    host = request.host
    if host.startswith("www."):
        return redirect(request.url.replace("www.", "", 1), code=301)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
