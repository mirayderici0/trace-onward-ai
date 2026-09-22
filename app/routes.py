from flask import Blueprint, jsonify, render_template, request

from app.database import lead_ekle, tum_leadler
from app.services.ai_service import AIServiceError, ai_service


# Web sayfaları için Blueprint
pages_bp = Blueprint("pages", __name__)

# API adresleri için Blueprint
api_bp = Blueprint("api", __name__, url_prefix="/api")


@pages_bp.route("/")
def ana_sayfa():
    """
    TRACE ONWARD ana sayfasını gösterir.
    """
    return render_template("index.html")


@pages_bp.route("/dashboard")
def dashboard():
    """
    Lead kayıtlarının görüleceği yönetim sayfasını gösterir.
    """
    return render_template("dashboard.html")


@api_bp.route("/sohbet", methods=["POST"])
def sohbet():
    """
    Kullanıcı mesajını AI servisine gönderir.
    """
    veri = request.get_json(silent=True) or {}

    mesaj = str(veri.get("message", "")).strip()
    gecmis = veri.get("history", [])

    if not mesaj:
        return jsonify({
            "basari": False,
            "hata": "message alanı zorunludur."
        }), 400

    if not isinstance(gecmis, list):
        gecmis = []

    try:
        yanit = ai_service.yanit_uret(
            mesaj,
            gecmis
        )

        return jsonify({
            "basari": True,
            "response": yanit
        }), 200

    except AIServiceError as hata:
        return jsonify({
            "basari": False,
            "hata": str(hata)
        }), 503


@api_bp.route("/leads", methods=["POST"])
def lead_olustur():
    """
    Yeni lead kaydını veritabanına ekler.
    """
    veri = request.get_json(silent=True) or {}

    isim = str(veri.get("name", "")).strip()
    telefon = str(veri.get("phone", "")).strip()
    mesaj = str(veri.get("message", "")).strip() or None

    if not isim or not telefon:
        return jsonify({
            "basari": False,
            "hata": "name ve phone alanları zorunludur."
        }), 400

    try:
        kayit_id = lead_ekle(
            isim,
            telefon,
            mesaj
        )

        return jsonify({
            "basari": True,
            "id": kayit_id,
            "mesaj": "İletişim bilgileri kaydedildi."
        }), 201

    except Exception:
        return jsonify({
            "basari": False,
            "hata": "Kayıt oluşturulurken bir hata oluştu."
        }), 500


@api_bp.route("/leads", methods=["GET"])
def leadleri_listele():
    """
    Kayıtlı tüm leadleri JSON olarak döndürür.
    """
    try:
        kayitlar = tum_leadler()

        leadler = []

        for kayit in kayitlar:
            leadler.append({
                "id": kayit["id"],
                "name": kayit["isim"],
                "phone": kayit["telefon"],
                "message": kayit["mesaj"],
                "date": kayit["tarih"]
            })

        return jsonify({
            "basari": True,
            "leads": leadler
        }), 200

    except Exception:
        return jsonify({
            "basari": False,
            "hata": "Kayıtlar alınırken bir hata oluştu."
        }), 500