import requests

from config import Config


class AIServiceError(Exception):
    """
    Yapay zeka servisi ile ilgili hatalar için özel hata sınıfı.
    """
    pass


class AIService:
    """
    TRACE ONWARD yapay zeka servisini yönetir.
    """

    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.business_context = Config.BUSINESS_CONTEXT
        self.model = "openai/gpt-oss-20b"

    def sistem_mesaji(self):
        """
        Yapay zekanın kimliğini ve görevini döndürür.
        """
        return self.business_context

    def yanit_uret(self, mesaj, gecmis=None):
        """
        Kullanıcı mesajını Groq API'ye gönderir
        ve yapay zeka yanıtını döndürür.
        """

        if not mesaj:
            raise AIServiceError("Mesaj boş olamaz.")

        if gecmis is None:
            gecmis = []

        # API anahtarı yoksa uygulama çökmesin.
        if not self.api_key:
            return (
                "TRACE ONWARD demo modu aktif. "
                "Yapay zeka bağlantısı için API anahtarı gereklidir."
            )

        messages = [
            {
                "role": "system",
                "content": self.sistem_mesaji()
            }
        ]

        # Önce geçmiş konuşmaları ekliyoruz.
        for kayit in gecmis:
            if (
                isinstance(kayit, dict)
                and "role" in kayit
                and "content" in kayit
            ):
                messages.append(kayit)

        # En sona yeni kullanıcı mesajı gelir.
        messages.append(
            {
                "role": "user",
                "content": mesaj
            }
        )

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        veri = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.4
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=veri,
                timeout=30
            )

            response.raise_for_status()

            sonuc = response.json()

            return sonuc["choices"][0]["message"]["content"]

        except requests.RequestException as hata:
            raise AIServiceError(
                "Yapay zeka servisine bağlanırken bir hata oluştu."
            ) from hata

        except (KeyError, IndexError, TypeError) as hata:
            raise AIServiceError(
                "Yapay zeka servisinden beklenmeyen bir yanıt geldi."
            ) from hata


ai_service = AIService()