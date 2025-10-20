from flask import Flask, render_template, request, redirect, url_for
from flask_babel import Babel
import os
from routes.main_routes import main_bp
from routes.contact_routes import contact_bp
from routes.blog_routes import blog_bp
from routes.sitemap_routes import sitemap_bp
from routes.admin_routes import admin_bp

# ------------------------------------------------------
# Flask Configuration
# ------------------------------------------------------
app = Flask(__name__, template_folder="templates", static_folder="static")

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret_key")
app.config["BABEL_DEFAULT_LOCALE"] = "en"
app.config["BABEL_TRANSLATION_DIRECTORIES"] = "locales"

babel = Babel(app)

# Supported languages
LANGUAGES = {"en": "English", "es": "Español", "pt": "Português"}

@babel.localeselector
def get_locale():
    # Detect user language from URL query or browser settings
    return request.args.get("lang") or request.accept_languages.best_match(LANGUAGES.keys())

# ------------------------------------------------------
# Blueprints registration
# ------------------------------------------------------
app.register_blueprint(main_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(sitemap_bp)
app.register_blueprint(admin_bp)

# ------------------------------------------------------
# Error handlers
# ------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

# ------------------------------------------------------
# Run Application
# ------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
