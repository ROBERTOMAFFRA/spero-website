from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from flask_mail import Mail, Message

app = Flask(__name__)

# =============================
# EMAIL CONFIG (SendGrid)
# =============================
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'  # padrão SendGrid
app.config['MAIL_PASSWORD'] = os.getenv('SENDGRID_API_KEY')  # variável no Render
app.config['MAIL_DEFAULT_SENDER'] = 'contact@spero-restoration.com'

mail = Mail(app)

# =============================
# ROTAS PRINCIPAIS
# =============================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = Message(
            subject=f"New Contact Form Submission from {name}",
            sender='contact@spero-restoration.com',
            recipients=[
                'contact@spero-restoration.com',
                'roberto.maffra@gmail.com'
            ],
            body=f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
        )

        mail.send(msg)
        return redirect(url_for('thank_you'))

    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return "Internal Server Error", 500

@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

# =============================
# SEO FILES (robots.txt & sitemap.xml)
# =============================
@app.route('/robots.txt')
def robots():
    return send_from_directory('.', 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')

# =============================
# EXECUÇÃO LOCAL
# =============================
if __name__ == '__main__':
    app.run(debug=True)
