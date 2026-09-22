import os

from flask import Flask, jsonify
from flask_cors import CORS

from config import config_by_name
from app.database import init_db
from app.routes import api_bp, pages_bp


def create_app():
    """
    Flask uygulamasını oluşturur ve gerekli modülleri bağlar.
    """

    app = Flask(__name__)

    environment = os.environ.get(
        "FLASK_ENV",
        "development"
    )

    config_class = config_by_name.get(
        environment,
        config_by_name["development"]
    )

    app.config.from_object(config_class)

    # Wix ve diğer izin verilen istemcilerin API'ye erişebilmesini sağlar.
    allowed_origins = [
        origin.strip()
        for origin in app.config["CORS_ORIGINS"].split(",")
        if origin.strip()
    ]

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": allowed_origins
            }
        }
    )

    # Veritabanını hazırlar.
    init_db(app)

    # Sayfa ve API route'larını uygulamaya bağlar.
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)

    @app.route("/health")
    def health():
        return jsonify({
            "basari": True,
            "durum": "ok",
            "uygulama": "TRACE ONWARD"
        }), 200

    return app