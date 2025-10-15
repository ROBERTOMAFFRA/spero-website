from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# 🔧 Configuração básica de envio de email (usando SMTP)
EMAIL_USER = os.getenv("EMAIL_USER", "contact@spero-restoration.com")
EMAIL_PASS = os.getenv("EMAIL_PASS", "your-email-password")
EMAIL_TO = os.getenv("EMAIL_TO", "contact@spero-restoration.com")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

# 📬 Endpoint para captura de leads
@app.route('/send', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_TO
        msg['Subject'] = f"New Lead from Spero Website: {name}"

        body = f"""
        Name: {name}
        Email: {email}
        Message:
        {message}
        """
        msg.attach(MIMEText(body, 'plain'))

        # Envio via servidor SMTP (Zoho / Outlook)
        with smtplib.SMTP('smtp.zoho.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        return jsonify({"success": True}), 200
    except Exception as e:
        print("❌ Error sending email:", e)
        return jsonify({"success": False, "error": str(e)}), 500


# 🔍 SEO + Sitemap + Robots
@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return app.send_static_file('sitemap.xml')


# 🔥 Render Ready
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
