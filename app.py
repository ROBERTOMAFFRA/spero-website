import os
import json
from datetime import datetime
from pathlib import Path
from flask import (
    Flask, render_template, request, redirect, url_for,
    send_from_directory, flash, session
)
from werkzeug.utils import secure_filename

# -----------------------
# App & Paths
# -----------------------
app = Flask(__name__)

# Secret key (use a strong one in Render env)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "changeme-in-render")

# Upload folder (kept under /static/images/uploads as alinhado no projeto)
UPLOAD_FOLDER = Path(app.static_folder) / "images" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)

# Testimonials file (mantém compatibilidade; usa JSON e também lê TXT se existir)
DATA_DIR = Path("./data")
DATA_DIR.mkdir(exist_ok=True)
TESTIMONIALS_JSON = DATA_DIR / "testimonials.json"
TESTIMONIALS_TXT = DATA_DIR / "testimonials.txt"  # legado (opcional)

# Translations (pasta /translations como no seu repositório)
TRANSLATION_PATH = Path("./translations")

# Company settings
COMPANY_PHONE = "(407) 724-6310"
COMPANY_PHONE_TEL = "+14077246310"
COMPANY_EMAIL = os.getenv("SENDER_EMAIL", "contact@spero-restoration.com")
COMPANY_NAME = "Spero Restoration Corp"
SERVICE_AREAS = ["Orlando", "Windermere", "Lake Nona", "Winter Garden", "Clermont"]

# SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
ADMIN_RECIPIENTS = [
    "contact@spero-restoration.com",
    "roberto.maffra@gmail.com",
]

# Admin login
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "RobertoMaffra")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "spero2025admin")


# -----------------------
# Utilities
# -----------------------
def load_translations(lang_code: str) -> dict:
    """Load translation JSON from /translations (fallback to 'en')."""
    code = (lang_code or "en").lower()
    candidate = TRANSLATION_PATH / f"{code}.json"
    if not candidate.exists():
        candidate = TRANSLATION_PATH / "en.json"
    try:
        with candidate.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def get_lang():
    # Priority: ?lang=xx → session → default 'en'
    lang = request.args.get("lang")
    if lang:
        session["lang"] = lang
    return session.get("lang", "en")

@app.context_processor
def inject_globals():
    lang = get_lang()
    tmap = load_translations(lang)

    def t(key, default=None):
        return tmap.get(key, default if default is not None else key)

    return dict(
        t=t,
        lang=lang,
        phone=COMPANY_PHONE,
        phone_tel=COMPANY_PHONE_TEL,
        company_name=COMPANY_NAME,
        company_email=COMPANY_EMAIL,
        service_areas=SERVICE_AREAS,
    )

def list_before_after_pairs():
    """
    Build a list of dicts with 'before' and 'after' filenames found under static/images/uploads.
    Pairing rule:
      - files named with 'before' and 'after' tokens are paired by common prefix before the token.
      - otherwise they are ignored for pairing.
    """
    files = [f for f in UPLOAD_FOLDER.iterdir() if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]]
    # Normalize to lowercase names for matching
    before_map = {}
    after_map = {}
    for p in files:
        name = p.name
        lname = name.lower()
        stem = p.stem.lower()
        if "before" in lname:
            key = stem.replace("before", "").replace("-", "_").replace(" ", "_")
            before_map[key] = name
        elif "after" in lname:
            key = stem.replace("after", "").replace("-", "_").replace(" ", "_")
            after_map[key] = name

    pairs = []
    for key, bname in before_map.items():
        aname = after_map.get(key)
        if aname:
            pairs.append({"before": bname, "after": aname})
    # sort for consistent display
    pairs.sort(key=lambda x: x["before"].lower())
    return pairs

def load_testimonials():
    """Load testimonials from JSON; if missing, try legacy txt (name|stars|message)."""
    items = []
    if TESTIMONIALS_JSON.exists():
        try:
            with TESTIMONIALS_JSON.open("r", encoding="utf-8") as f:
                items = json.load(f)
        except Exception:
            items = []

    elif TESTIMONIALS_TXT.exists():
        try:
            with TESTIMONIALS_TXT.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split("|", 2)
                    if len(parts) == 3:
                        name, stars, msg = parts
                        try:
                            stars = int(stars)
                        except Exception:
                            stars = 5
                        items.append({"name": name, "stars": stars, "message": msg})
        except Exception:
            pass

    # sanitize stars
    for r in items:
        r["stars"] = max(1, min(5, int(r.get("stars", 5) or 5)))
        r["name"] = (r.get("name") or "").strip()
        r["message"] = (r.get("message") or "").strip()

    return items

def save_testimonial(name, stars, message):
    items = load_testimonials()
    items.append({
        "name": name.strip(),
        "stars": max(1, min(5, int(stars))),
        "message": message.strip(),
        "created_at": datetime.utcnow().isoformat()
    })
    with TESTIMONIALS_JSON.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def send_emails_via_sendgrid(subject, html_body, to_list, reply_to=None):
    """Send email using SendGrid API if key is set."""
    if not SENDGRID_API_KEY:
        return False, "SENDGRID_API_KEY not configured"

    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail, Email, To, ReplyTo

        message = Mail(
            from_email=Email(COMPANY_EMAIL, COMPANY_NAME),
            to_emails=[To(addr) for addr in to_list],
            subject=subject,
            html_content=html_body
        )
        if reply_to:
            message.reply_to = ReplyTo(reply_to)

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        _ = sg.send(message)
        return True, "sent"
    except Exception as e:
        return False, str(e)


# -----------------------
# Routes - Core Pages
# -----------------------
@app.route("/")
def index():
    pairs = list_before_after_pairs()
    testimonials = load_testimonials()
    return render_template(
        "index.html",
        title="Spero Restoration Corp — Orlando",
        pairs=pairs,
        testimonials=testimonials
    )

@app.route("/about")
def about():
    return render_template("about.html", title="About | Spero Restoration")

@app.route("/services")
def services():
    return render_template("services.html", title="Services | Spero Restoration")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        service = request.form.get("service", "").strip()
        message = request.form.get("message", "").strip()

        if not (name and email and phone and message):
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("contact"))

        # Email to admins
        admin_subject = f"[Spero] New Contact — {name}"
        admin_body = f"""
        <h3>New Contact Request</h3>
        <p><b>Name:</b> {name}</p>
        <p><b>Email:</b> {email}</p>
        <p><b>Phone:</b> {phone}</p>
        <p><b>Service:</b> {service}</p>
        <p><b>Message:</b><br>{message}</p>
        <hr><p>Website: spero-restoration.com</p>
        """
        ok_admin, _ = send_emails_via_sendgrid(admin_subject, admin_body, ADMIN_RECIPIENTS, reply_to=email)

        # Confirmation to customer
        customer_subject = "Spero Restoration — We received your request"
        customer_body = f"""
        <p>Hi {name},</p>
        <p>Thanks for reaching out to <b>Spero Restoration Corp</b>. Our team will contact you shortly.</p>
        <p>If it's urgent, call us at <a href="tel:{COMPANY_PHONE_TEL}">{COMPANY_PHONE}</a>.</p>
        <p>— Spero Restoration Corp</p>
        """
        ok_user, _ = send_emails_via_sendgrid(customer_subject, customer_body, [email])

        if ok_admin:
            flash("Thanks! Your message has been sent. Our team will reach out shortly.", "success")
        else:
            flash("We could not send the email at this moment. Please try again or call us.", "error")

        return redirect(url_for("contact"))

    return render_template("contact.html", title="Contact | Spero Restoration")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html", title="Privacy Policy | Spero Restoration")

@app.route("/terms")
def terms():
    return render_template("terms.html", title="Terms of Service | Spero Restoration")

# Serve robots/sitemap directly from project root if needed
@app.route("/robots.txt")
def robots():
    return send_from_directory(Path("."), "robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory(Path("."), "sitemap.xml")


# -----------------------
# Admin Area
# -----------------------
def admin_logged_in():
    return session.get("admin_logged_in") is True

@app.route("/admin", methods=["GET"])
def admin_home():
    """Unificado: se logado, mostra dashboard; senão, mostra login dentro do admin.html"""
    photo_pairs = list_before_after_pairs() if admin_logged_in() else []
    testimonials = load_testimonials() if admin_logged_in() else []
    return render_template("admin.html", photo_pairs=photo_pairs, testimonials=testimonials)

@app.route("/admin/login", methods=["POST"])
def admin_login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session["admin_logged_in"] = True
        return redirect(url_for("admin_home"))
    flash("Invalid credentials.", "error")
    return redirect(url_for("admin_home"))

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_home"))

@app.route("/admin/upload", methods=["POST"])
def upload_photo():
    if not admin_logged_in():
        return redirect(url_for("admin_home"))

    before_file = request.files.get("before_photo")
    after_file = request.files.get("after_photo")

    if not (before_file and after_file):
        flash("Please select both Before and After images.", "error")
        return redirect(url_for("admin_home"))

    # secure filenames
    before_name = secure_filename(before_file.filename)
    after_name = secure_filename(after_file.filename)

    if not before_name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        flash("Invalid file type for Before image.", "error")
        return redirect(url_for("admin_home"))
    if not after_name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        flash("Invalid file type for After image.", "error")
        return redirect(url_for("admin_home"))

    before_path = UPLOAD_FOLDER / before_name
    after_path = UPLOAD_FOLDER / after_name
    before_file.save(before_path)
    after_file.save(after_path)

    flash("Images uploaded successfully.", "success")
    return redirect(url_for("admin_home"))

@app.route("/admin/testimonial", methods=["POST"])
def add_testimonial():
    if not admin_logged_in():
        return redirect(url_for("admin_home"))
    name = request.form.get("name", "").strip()
    message = request.form.get("message", "").strip()
    stars = request.form.get("stars", "5").strip()
    if not (name and message):
        flash("Please fill the name and message.", "error")
        return redirect(url_for("admin_home"))
    try:
        save_testimonial(name, int(stars), message)
        flash("Testimonial added.", "success")
    except Exception as e:
        flash(f"Could not save testimonial: {e}", "error")
    return redirect(url_for("admin_home"))


# -----------------------
# Error handlers
# -----------------------
@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    # For local dev only; Render uses Procfile/gunicorn
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
