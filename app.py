from flask import Flask, render_template, request, jsonify
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página de agradecimento (opcional)
@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

# Rota de envio do formulário
@app.route('/send', methods=['POST'])
def send_email():
    try:
        name = request.form.get('name', 'Visitor')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        # Verificar se há informações obrigatórias
        if not email or not message:
            return jsonify({'success': False, 'message': 'Please fill in all required fields.'})

        # Monta o conteúdo do e-mail
        subject = f"New Inspection Request from {name}"
        content = f"""
        <h3>Inspection Request Details</h3>
        <p><b>Name:</b> {name}</p>
        <p><b>Email:</b> {email}</p>
        <p><b>Phone:</b> {phone}</p>
        <p><b>Message:</b> {message}</p>
        """

        # Chaves do ambiente (Render)
        sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
        from_email = os.getenv('FROM_EMAIL', 'contact@spero-restoration.com')
        to_email = os.getenv('TO_EMAIL', 'roberto.maffra@gmail.com')

        # Envia via SendGrid
        message = Mail(
            from_email=from_email,
            to_emails=[to_email, from_email],  # Cópia para os dois
            subject=subject,
            html_content=content
        )

        sg = SendGridAPIClient(sendgrid_api_key)
        sg.send(message)

        return jsonify({'success': True, 'message': 'Email sent successfully!'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred while sending the email.'})


# Executar localmente (modo debug)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

