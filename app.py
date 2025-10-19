from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# === HOME PAGE ===
@app.route('/')
def index():
    return render_template('index.html')

# === ABOUT PAGE ===
@app.route('/about')
def about():
    return render_template('about.html')

# === SERVICES PAGE ===
@app.route('/services')
def services():
    return render_template('services.html')

# === CONTACT PAGE ===
@app.route('/contact')
def contact():
    return render_template('contact.html')

# === THANK YOU PAGE (after form submission) ===
@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

# === PRIVACY POLICY PAGE ===
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# === TERMS PAGE ===
@app.route('/terms')
def terms():
    return render_template('terms.html')

# === SEND EMAIL (dummy placeholder) ===
@app.route('/send', methods=['POST'])
def send():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')

    print(f"Form submitted by {name} ({email}, {phone}): {message}")

    # In production, integrate SendGrid or SMTP here
    return redirect(url_for('thank_you'))

# === CUSTOM 404 PAGE ===
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

# === MAIN ENTRY POINT ===
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
