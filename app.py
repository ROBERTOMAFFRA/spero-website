
from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.zoho.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'contact@spero-restoration.com'
app.config['MAIL_PASSWORD'] = 'YOUR_ZOHO_PASSWORD'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    msg = Message(f"New message from {name}",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=['contact@spero-restoration.com', 'roberto.maffra@gmail.com'])
    msg.body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

    mail.send(msg)
    return render_template('index.html', success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
