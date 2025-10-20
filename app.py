from flask import Flask, render_template, request, redirect, url_for, flash
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "spero_secure_key")

# ==== CONFIG SENDGRID ====
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "contact@spero-restoration.com")
ADMIN_EMAIL = "roberto.maffra@gmail.com"

# ==== UPLOADS ====
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ==== ROUTES ====

@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        subject = f"Website Message from {name}"
        body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

        try:
            msg = MIMEMultipart()
            msg["From"] = CONTACT_EMAIL
            msg["To"] = CONTACT_EMAIL
            msg["Cc"] = ADMIN_EMAIL
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP("smtp.sendgrid.net", 587)
            server.starttls()
            server.login("apikey", SENDGRID_API_KEY)
            server.sendmail(CONTACT_EMAIL, [CONTACT_EMAIL, ADMIN_EMAIL], msg.as_string())
            server.quit()

            flash("Message sent successfully!", "success")
            return redirect(url_for("contact"))
        except Exception as e:
            flash(f"Error sending email: {str(e)}", "danger")

    return render_template("contact.html")


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    error = None
    admin_user = os.getenv("ADMIN_USER", "RobertoMaffra")
    admin_pass = os.getenv("ADMIN_PASSWORD", "SperoSecure!2025")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == admin_user and password == admin_pass:
            flash("Welcome, admin!", "success")
            return redirect(url_for("index_page"))
        else:
            error = "Invalid username or password"
            flash(error, "danger")

    return render_template("admin_login.html", error=error)


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
