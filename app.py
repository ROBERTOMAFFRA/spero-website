from flask import Flask, render_template, url_for, redirect
import os

# Inicializa o app com caminhos corretos
app = Flask(__name__, static_folder="static", template_folder="templates")

# Variável de ambiente controla se o site está em manutenção
MAINTENANCE_MODE = os.getenv("MAINTENANCE_MODE", "on")  # 'on' ou 'off'

@app.route("/")
def home():
    # Se estiver em manutenção, mostra página especial
    if MAINTENANCE_MODE.lower() == "on":
        return render_template("maintenance.html")
    return render_template("index.html")

# Rota de visualização privada para revisão
@app.route("/preview")
def preview():
    return render_template("index.html")

# Sitemap e robots continuam automáticos
@app.route("/sitemap.xml")
def sitemap():
    return app.send_static_file("sitemap.xml")

@app.route("/robots.txt")
def robots():
    return app.send_static_file("robots.txt")

# Página 404 amigável
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
