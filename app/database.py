import sqlite3

from flask import current_app, g


def get_db():
    """
    Aktif veritabanı bağlantısını döndürür.
    Aynı istek boyunca tek bağlantı kullanılır.
    """
    if "db" not in g:
        database_path = current_app.config.get(
            "DATABASE_URL",
            "trace_onward.db"
        )

        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error=None):
    """
    İstek tamamlandığında veritabanı bağlantısını kapatır.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db(app):
    """
    Leads tablosunu yoksa oluşturur.
    """
    app.teardown_appcontext(close_db)

    with app.app_context():
        db = get_db()

        db.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        db.commit()


def lead_ekle(isim, telefon, mesaj=None):
    """
    Yeni bir kullanıcı kaydını güvenli biçimde veritabanına ekler.
    """
    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO leads (isim, telefon, mesaj)
        VALUES (?, ?, ?)
        """,
        (isim, telefon, mesaj)
    )

    db.commit()

    return cursor.lastrowid


def tum_leadler():
    """
    Tüm kullanıcı kayıtlarını en yeniden en eskiye döndürür.
    """
    db = get_db()

    kayitlar = db.execute(
        """
        SELECT id, isim, telefon, mesaj, tarih
        FROM leads
        ORDER BY id DESC
        """
    ).fetchall()

    return [dict(kayit) for kayit in kayitlar]