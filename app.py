from flask import Flask, render_template, send_from_directory, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# ============================================================
# 🔧 CONFIGURAÇÕES GERAIS
# ============================================================
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# ============================================================
# 🔒 MODO MANUTENÇÃO (ativo)
# ============================================================
@app.route('/')
def home():
    # Exibe página de manutenção (503)
    return render_template('maintenance.html'), 503

# ============================================================
# 📜 PÁGINAS SECUNDÁRIAS (ativas no backend, mas ocultas)
# ============================================================
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# ============================================================
# 🤖 ARQUIVOS TÉCNICOS
# ============================================================
@app.route('/robots.txt')
def robots_txt():
    return send_from_directory('.', 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    pages = [
        {'loc': 'https://spero-restoration.com/'},
        {'loc': 'https://spero-restoration.com/index'},
        {'loc': 'https://spero-restoration.com/terms'},
        {'loc': 'https://spero-restoration.com/privacy'}
    ]
    lastmod = datetime.now().date()
    return render_template('sitemap_template.xml', pages=pages, lastmod=lastmod), 200, {
        'Content-Type': 'application/xml'
    }

# ============================================================
# 🛠️ ERROS PADRONIZADOS
# ============================================================
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(503)
def maintenance_error(error):
    return render_template('maintenance.html'), 503

# ============================================================
# 🚀 EXECUÇÃO LOCAL
# ============================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
