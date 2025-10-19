import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import sendgrid
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "spero_secret_2025"

# Diretórios
UPLOAD_FOLDER = "static/images/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Credenciais Admin
ADMIN_USERNAME = "RobertoMaffra"
ADMIN_PASSWORD = "spero2025admin"

# Configuração SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
TO_EMAILS = ["contact@spero-restoration.com", "roberto.maffra@gmail.com"]
FROM_EMAIL = "contact@spero-restoration.com"

# ----------------------------------------------
# Funções auxiliares
# ----------------------------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email(subject, html_content, recipient):
    """Envio de e-mail via SendGrid"""
    if not SENDGRID_API_KEY:
        print("⚠️ SENDGRID_API_KEY não configurada.")
        return
    try:
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=recipient,
            subject=subject,
            html_content=html_content
        )
        sg.send(message)
        print(f"✅ E-mail enviado para {recipient}")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")

# ----------------------------------------------
# Textos multilíngues
# ----------------------------------------------
texts = {
    "en": {
        "home_title": "Restoration & Remodeling Experts",
        "home_subtitle": "Water Damage • Mold • Fire • Remodeling — Serving Orlando & Surrounding Areas",
        "cta": "Schedule Inspection",
        "gallery": "Before & After Projects",
        "reviews": "What Our Clients Say",
        "contact": "Contact Us",
        "form_success": "Thank you! We’ll contact you shortly.",
    },
    "es": {
        "home_title": "Expertos en Restauración y Remodelación",
        "home_subtitle": "Daños por Agua • Moho • Fuego • Remodelación — Sirviendo a Orlando y sus alrededores",
        "cta": "Programar Inspección",
        "gallery": "Proyectos Antes y Después",
        "reviews": "Lo Que Dicen Nuestros Clientes",
        "contact": "Contáctenos",
        "form_success": "¡Gracias! Nos pondremos en contacto pronto.",
    },
    "pt": {
        "home_title": "Especialistas em Restauração e Reforma",
        "home_subtitle": "Danos por Água • Mofo • Fogo • Reforma — Atendendo Orlando e Região",
        "cta": "Agendar Inspeção",
        "gallery": "Projetos Antes e Depois",
        "reviews": "O Que Nossos Clientes Dizem",
        "contact": "Fale Conosco",
        "form_success": "Obrigado! Entraremos em contato em breve.",
    }
}

# ----------------------------------------------
# Rotas públicas
# ----------------------------------------------
@app.route("/")
def index():
    lang = request.args.get("lang", "en")
    content = texts.get(lang, texts["en"])

    # Carrega imagens
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    image_files = sorted(os.listdir(UPLOAD_FOLDER))
    before_images = [img for img in image_files if "before" in img.lower()]
    after_images = [img for img in image_files if "after" in img.lower()]

    # Carrega reviews
    testimonials = []
    if os.path.exists("testimonials.txt"):
        with open("testimonials.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    testimonials.append({"name": parts[0], "review": parts[1], "stars": int(parts[2])})

    return render_template("index.html", lang=lang, content=content,
                           before_images=before_images, after_images=after_images,
                           testimonials=testimonials)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    lang = request.args.get("lang", "en")
    content = texts.get(lang, texts["en"])

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        service = request.form.get("service")
        message = request.form.get("message")

        subject = f"New Contact Request from {name}"
        html_content = f"""
        <h3>New Message from Website</h3>
        <p><b>Name:</b> {name}</p>
        <p><b>Email:</b> {email}</p>
        <p><b>Phone:</b> {phone}</p>
        <p><b>Service:</b> {service}</p>
        <p><b>Message:</b> {message}</p>
        """

        # Envia e-mails internos
        for admin_email in TO_EMAILS:
            send_email(subject, html_content, admin_email)

        # Confirmação para o cliente
        confirmation_html = f"""
        <h2>Thank you for contacting Spero Restoration!</h2>
        <p>We have received your request and will contact you soon.</p>
        <p><b>Your Message:</b><br>{message}</p>
        <p>— Spero Restoration Corp</p>
        """
        send_email("Confirmation – Spero Restoration", confirmation_html, email)

        flash(content["form_success"], "success")
        return redirect(url_for("contact", lang=lang))

    return render_template("contact.html", content=content, lang=lang)

# ----------------------------------------------
# Rotas de autenticação e painel
# ----------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USERNAME and request.form["password"] == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("admin"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("index"))

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST":
        # Upload de imagem
        if "file" in request.files:
            file = request.files["file"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                flash("Image uploaded successfully!", "success")

        # Adicionar review
        if "review" in request.form:
            name = request.form["name"]
            review = request.form["review"]
            stars = request.form["stars"]
            with open("testimonials.txt", "a", encoding="utf-8") as f:
                f.write(f"{name}|{review}|{stars}\n")
            flash("Review added successfully!", "success")

            send_email(
                "New Review Added",
                f"<p><b>{name}</b> added a review: “{review}” ({stars}⭐)</p>",
                TO_EMAILS
            )

    return render_template("admin.html")

# ----------------------------------------------
# SEO e Páginas padrão
# ----------------------------------------------
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

# ----------------------------------------------
# Execução
# ----------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
