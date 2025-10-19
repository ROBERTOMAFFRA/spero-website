import os
import io
import base64
import sqlite3
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect, url_for,
    send_from_directory, session, abort, jsonify, send_file
)
import requests
from werkzeug.utils import secure_filename

# =========================
#  CONFIGURAÇÃO BÁSICA
# =========================
app = Flask(__name__)

# Chaves e credenciais via ambiente
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-me-in-prod")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
FROM_EMAIL = "contact@spero-restoration.com"
TO_EMAILS = ["contact@spero-restoration.com", "roberto.maffra@gmail.com"]

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "RobertoMaffra")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "spero2025!")

# Pastas de dados
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
DB_PATH = os.path.join(DATA_DIR, "requests.db")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =========================
#  BANCO DE DADOS
# =========================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT,
            service TEXT,
            message TEXT,
            photo_before TEXT,
            photo_after TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

init_db()

# =========================
#  HELPERS
# =========================
def sendgrid_send(to_email: str, subject: str, content_text: str, attachments=None):
    """
    Envia e-mail com SendGrid API.
    attachments: lista de dicionários no formato SendGrid:
        {"content": base64_str, "filename": "file.xlsx", "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "disposition": "attachment"}
    """
    payload = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": FROM_EMAIL, "name": "Spero Restoration"},
        "subject": subject,
        "content": [{"type": "text/plain", "value": content_text}],
    }
    if attachments:
        payload["attachments"] = attachments

    r = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {SENDGRID_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=20,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"SendGrid error {r.status_code}: {r.text}")

def make_request_excel_row(record: dict) -> bytes:
    """
    Gera um arquivo Excel (.xlsx) em memória com UMA linha (o pedido recém-enviado).
    Retorna os bytes do arquivo.
    """
    # Geração leve sem depender de engine pesado:
    try:
        from openpyxl import Workbook
    except ImportError:
        # Segurança: caso openpyxl não esteja instalado
        raise RuntimeError("openpyxl não instalado. Adicione ao requirements.txt")

    wb = Workbook()
    ws = wb.active
    ws.title = "Inspection Request"

    headers = [
        "ID", "Name", "Email", "Phone", "Address",
        "Service", "Message", "Status", "Created At",
        "Photo Before", "Photo After"
    ]
    ws.append(headers)

    ws.append([
        record.get("id"),
        record.get("name"),
        record.get("email"),
        record.get("phone"),
        record.get("address"),
        record.get("service"),
        record.get("message"),
        record.get("status"),
        record.get("created_at"),
        record.get("photo_before"),
        record.get("photo_after"),
    ])

    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream.read()

def save_upload(file_storage):
    """
    Salva upload na pasta data/uploads e retorna caminho relativo (filename).
    """
    if not file_storage or not file_storage.filename:
        return ""
    filename = secure_filename(file_storage.filename)
    base, ext = os.path.splitext(filename)
    unique_name = f"{base}_{int(datetime.utcnow().timestamp())}{ext or '.jpg'}"
    full_path = os.path.join(UPLOAD_DIR, unique_name)
    file_storage.save(full_path)
    return unique_name  # armazenamos só o nome do arquivo

def require_admin():
    if not session.get("admin_logged"):
        abort(403)

# =========================
#  ROTAS PÚBLICAS
# =========================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/thank-you")
def thank_you():
    return render_template("thank-you.html")

# Uploads públicos (para admin visualizar imagens gravadas)
@app.route("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory(UPLOAD_DIR, filename)

# Formulário de contato / inspeção
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        service = request.form.get("service", "").strip()
        message = request.form.get("message", "").strip()

        photo_before = request.files.get("photo_before")
        photo_after = request.files.get("photo_after")

        # Salva uploads (se houver)
        before_filename = save_upload(photo_before)
        after_filename  = save_upload(photo_after)

        created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        # Grava no banco
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO requests
            (name, email, phone, address, service, message, photo_before, photo_after, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending', ?)
            """,
            (name, email, phone, address, service, message, before_filename, after_filename, created_at),
        )
        conn.commit()
        new_id = cur.lastrowid
        conn.close()

        # Cria conteúdo do e-mail
        admin_text = f"""
New Inspection Request
--------------------------
Name: {name}
Email: {email}
Phone: {phone}
Address: {address}
Service: {service}

Message:
{message}

Files:
Before: {before_filename or 'n/a'}
After : {after_filename or 'n/a'}

Submitted at (UTC): {created_at}
        """.strip()

        try:
            # Envia para cada destinatário (contact e roberto) com Excel do pedido
            # Gera Excel do registro (1 linha)
            # Busca o registro recém inserido:
            conn = get_db()
            row = conn.execute("SELECT * FROM requests WHERE id = ?", (new_id,)).fetchone()
            conn.close()
            record = dict(row) if row else {}

            xlsx_bytes = make_request_excel_row(record)
            xlsx_b64 = base64.b64encode(xlsx_bytes).decode("utf-8")
            attachments = [{
                "content": xlsx_b64,
                "filename": f"request_{new_id}.xlsx",
                "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "disposition": "attachment"
            }]

            for rcpt in TO_EMAILS:
                sendgrid_send(
                    to_email=rcpt,
                    subject=f"[Spero] New Inspection Request — {name}",
                    content_text=admin_text,
                    attachments=attachments
                )

            # Confirmação para o cliente (sem anexo)
            confirm_text = f"""
Hi {name},

Thank you for contacting Spero Restoration Corp.
We received your request regarding: {service}.
Our team will get in touch with you shortly at {phone}.

Best regards,
Spero Restoration Corp
(407) 724-6310
contact@spero-restoration.com
            """.strip()

            if email:
                sendgrid_send(
                    to_email=email,
                    subject="We received your request — Spero Restoration Corp",
                    content_text=confirm_text,
                    attachments=None
                )

            return render_template("contact.html", success=True)

        except Exception as e:
            print("Error sending email:", e)
            return render_template("contact.html", error=True)

    return render_template("contact.html")

# =========================
#  ÁREA ADMIN
# =========================
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        user = request.form.get("username", "")
        pwd = request.form.get("password", "")
        if user == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
            session["admin_logged"] = True
            return redirect(url_for("admin_dashboard"))
        return render_template("admin_login.html", error=True)
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged", None)
    return redirect(url_for("admin_login"))

@app.route("/admin/dashboard")
def admin_dashboard():
    require_admin()
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM requests ORDER BY datetime(created_at) DESC"
    ).fetchall()
    conn.close()
    return render_template("admin_dashboard.html", items=rows)

@app.route("/admin/status/<int:rid>", methods=["POST"])
def admin_update_status(rid):
    require_admin()
    new_status = request.form.get("status", "Pending")
    conn = get_db()
    conn.execute("UPDATE requests SET status = ? WHERE id = ?", (new_status, rid))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/export")
def admin_export_excel():
    require_admin()
    # Gera excel com TODOS os registros
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Requests"

    headers = [
        "ID","Name","Email","Phone","Address",
        "Service","Message","Status","Created At",
        "Photo Before","Photo After"
    ]
    ws.append(headers)

    conn = get_db()
    rows = conn.execute("SELECT * FROM requests ORDER BY datetime(created_at) DESC").fetchall()
    conn.close()

    for r in rows:
        ws.append([
            r["id"], r["name"], r["email"], r["phone"], r["address"],
            r["service"], r["message"], r["status"], r["created_at"],
            r["photo_before"], r["photo_after"]
        ])

    bio = io.BytesIO()
    wb.save(bio)
    bio.seek(0)
    filename = "Spero Restoration Corp — Inspection Requests.xlsx"
    return send_file(
        bio,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# =========================
#  SAÚDE / ERROS
# =========================
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.errorhandler(403)
def e403(_):
    return "Forbidden", 403

@app.errorhandler(404)
def e404(_):
    return "Not Found", 404

# =========================
#  MAIN
# =========================
if __name__ == "__main__":
    # Para ambiente local
    app.run(host="0.0.0.0", port=5000, debug=True)
