# ============================================================
# SPERO RESTORATION vFinal – SEO MASTER PLAN
# Main Flask Application Entry Point
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import Mail
from routes import main_routes, contact_routes, blog_routes, sitemap_routes, admin_routes

# ============================================================
# INITIAL CONFIGURATION
# ============================================================

load_dotenv()
app = Flask(__name__)

# Domain and Contact Config
app.config['DOMAIN'] = os.getenv("DOMAIN", "https://spero-restoration.com")
app.config['FROM_EMAIL'] = os.getenv("FROM_EMAIL", "contact@spero-restoration.com")
app.config['TO_EMAIL'] = os.getenv("TO_EMAIL", "contact@spero-restoration.com")
app.config['BCC_EMAIL'] = os.getenv("BCC_EMAIL", "roberto.maffra@gmail.com")
app.config['SENDGRID_API_KEY'] = os.getenv("SENDGRID_API_KEY")
app.config['GTM_ID'] = os.getenv("GTM_ID", "")

# ============================================================
# BLUEPRINTS REGISTRATION
# ============================================================

app.register_blueprint(main_routes.bp)
app.register_blueprint(contact_routes.bp)
app.register_blueprint(blog_routes.bp)
app.register_blueprint(sitemap_routes.bp)
app.register_blueprint(admin_routes.bp)

# ============================================================
# ROUTES (Fallback and Testing)
# ============================================================

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/contact', methods=['GET'])
def contact_page():
    """Render the contact form page."""
    return render_template('contact.html')

@app.route('/thankyou')
def thankyou_page():
    """Render the thank-you confirmation page."""
    return render_template('thankyou.html')

# ============================================================
# CONTACT FORM HANDLER (SendGrid Integration)
# ============================================================

@app.route('/send-email', methods=['POST'])
def send_email():
    """Handles email submissions via SendGrid."""
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        sg = sendgrid.SendGridAPIClient(api_key=app.config['SENDGRID_API_KEY'])
        content = f"""
        New contact from Spero Restoration website:
        ------------------------------------------
        Name: {name}
        Email: {email}
        Phone: {phone}
        Message: {message}
        """

        mail = Mail(
            from_email=app.config['FROM_EMAIL'],
            to_emails=app.config['TO_EMAIL'],
            subject=f"New Contact Form Submission from {name}",
            plain_text_content=content
        )

        # Add BCC (backup copy)
        if app.config['BCC_EMAIL']:
            mail.add_bcc(app.config['BCC_EMAIL'])

        sg.send(mail)

        return redirect(url_for('thankyou_page'))

    except Exception as e:
        print(f"SendGrid Error: {e}")
        return jsonify({"error": "Email not sent", "details": str(e)}), 500

# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# ============================================================
# ENTRY POINT
# ============================================================
@app.route('/maintenance')
def maintenance_mode():
    """Manual Maintenance Page"""
    return render_template('503.html'), 503

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
