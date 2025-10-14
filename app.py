from flask import Flask, render_template, request, redirect, url_for, flash
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "spero_secret_key")

# ✅ Rota principal
@app.route("/")
def home():
    return render_template("index.html")

# ✅ Página "Quem somos"
@app.route("/about")
def about():
    return render_template("about.html")

# ✅ Página "Política de Privacidade"
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

# ✅ Página "Termos de Uso"
@app.route("/terms")
def terms():
    return render_template("terms.html")

# ✅ Página de Agradecimento
@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

# ✅ Formulário de contato — SendGrid integrado
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not name or not email or not message:
        flash("Please fill out all fields before submitting.")
        return redirect(url_for("home"))

    try:
        # Configuração do SendGrid
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))

        # E-mail principal
        email_to = "contact@spero-restoration.com"
        msg = Mail(
            from_email="contact@spero-restoration.com",
            to_emails=email_to,
            subject=f"New message from {name} via website",
            html_content=f"""
            <strong>New contact form submission:</strong><br><br>
            <b>Name:</b> {name}<br>
            <b>Email:</b> {email}<br>
            <b>Message:</b><br>{message}
            """
        )
        sg.send(msg)

        # Cópia para você (Roberto)
        msg_copy = Mail(
            from_email="contact@spero-restoration.com",
            to_emails="roberto.maffra@gmail.com",
            subject=f"Copy of message from {name}",
            html_content=f"""
            <strong>Contact form submission copy:</strong><br><br>
            <b>Name:</b> {name}<br>
            <b>Email:</b> {email}<br>
            <b>Message:</b><br>{message}
            """
        )
        sg.send(msg_copy)

        return redirect(url_for("thankyou"))

    except Exception as e:
        print(f"Error sending email: {e}")
        flash("There was an error sending your message. Please try again later.")
        return redirect(url_for("home"))

# ✅ Para Render / produção
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
