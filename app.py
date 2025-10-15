from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from flask_mail import Mail, Message

app = Flask(__name__)

# =============================
# EMAIL CONFIG (ajuste se já configurado)
# =============================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # e-mail remetente
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # senha ou app password

mail = Mail(app)

# =============================
# ROTAS PRINCIPAIS
# =============================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    msg = Message(
        subject=f"New Contact Form Submission from {name}",
        sender=email,
        recipients=[os.getenv('MAIL_USERNAME')],
        body=f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
    )
    mail.send(msg)
    return redirect(url_for('thank_you'))

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
