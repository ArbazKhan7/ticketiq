from app.core.config import settings

def test_config():
    print("OpenAI Key Loaded:", bool(settings.openai_api_key))
    print("Twilio SID Loaded:", settings.twilio_account_sid[:6] + "...")
    print("Database URL Loaded:", settings.database_url.split("@")[0] + "@...")
    print("Redis URL Loaded:", settings.redis_url)

if __name__ == "__main__":
    test_config()
