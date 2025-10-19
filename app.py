from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os

# ========= Email (SendGrid) =========
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "contact@spero-restoration.com")
INTERNAL_RECIPIENTS = ["contact@spero-restoration.com", "roberto.maffra@gmail.com"]

def send_emails(name, email, phone, service, message):
    """
    Envia 2 e-mails:
      1) Interno: para contact@spero-restoration.com e roberto.maffra@gmail.com
      2) Confirmação para o cliente (email informado no formulário)
    Se não houver SENDGRID_API_KEY, apenas registra no log.
    """
    subject_internal = f"[Spero Website] New inspection request from {name}"
    body_internal = (
        f"New lead from the website:\n\n"
        f"Name: {name}\nEmail: {email}\nPhone: {phone}\nService: {service}\n\n"
        f"Message:\n{message}\n"
    )
    subject_client = "Spero Restoration — We received your request"
    body_client = (
        f"Hi {name},\n\nThanks for reaching out to Spero Restoration Corp!\n"
        f"We received your request and a specialist will contact you shortly.\n\n"
        f"Summary:\n- Service: {service}\n- Phone: {phone}\n- Message: {message}\n\n"
        f"Best regards,\nSpero Restoration Corp\nhttps://spero-restoration.com\n"
    )

    if not SENDGRID_API_KEY:
        print("[EMAIL][SIMULATION] No SENDGRID_API_KEY set.")
        print("[EMAIL][INTERNAL]", subject_internal, body_internal)
        print("[EMAIL][CLIENT]", subject_client, body_client)
        return

    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail, Email, To, Content, ReplyTo

        sg = SendGridAPIClient(SENDGRID_API_KEY)

        mail_internal = Mail(
            from_email=Email(FROM_EMAIL, "Spero Restoration"),
            to_emails=[To(addr) for addr in INTERNAL_RECIPIENTS],
            subject=subject_internal,
            plain_text_content=Content("text/plain", body_internal),
        )
        if email:
            mail_internal.reply_to = ReplyTo(email)
        sg.send(mail_internal)

        if email:
            mail_client = Mail(
                from_email=Email(FROM_EMAIL, "Spero Restoration"),
                to_emails=[To(email)],
                subject=subject_client,
                plain_text_content=Content("text/plain", body_client),
            )
            sg.send(mail_client)

        print("[EMAIL] Messages sent successfully via SendGrid.")
    except Exception as e:
        print(f"[EMAIL][ERROR] {e}")

# ========= Flask =========
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "spero_secret_key")

# ---- Páginas ----
@app.route("/")
def index():
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
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        service = request.form.get("service", "").strip()
        message = request.form.get("message", "").strip()

        send_emails(name, email, phone, service, message)
        flash("Thank you! We’ll contact you shortly.", "success")
        return redirect(url_for("thank_you"))

    return render_template("contact.html")

@app.route("/thank-you")
def thank_you():
    return render_template("thank-you.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

# ---- Servir robots/sitemap da raiz ----
@app.route("/robots.txt")
def robots():
    return send_from_directory(os.path.join(app.root_path), "robots.txt", mimetype="text/plain")

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory(os.path.join(app.root_path), "sitemap.xml", mimetype="application/xml")

# ---- 404 ----
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
