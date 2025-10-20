import os
from dotenv import load_dotenv

# ------------------------------------------------------
# Load environment variables
# ------------------------------------------------------
load_dotenv()

class Config:
    # --------------------------------------------------
    # Basic settings
    # --------------------------------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")

    # --------------------------------------------------
    # Domain and base URL
    # --------------------------------------------------
    DOMAIN = "https://spero-restoration.com"

    # --------------------------------------------------
    # Email (SendGrid)
    # --------------------------------------------------
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
    CONTACT_EMAIL = "contact@spero-restoration.com"
    BCC_EMAIL = "roberto.maffra@gmail.com"

    # --------------------------------------------------
    # Google Integrations
    # --------------------------------------------------
    GA4_ID = os.getenv("GA4_ID", "")
    GTM_ID = os.getenv("GTM_ID", "")
    GOOGLE_ADS_ID = os.getenv("GOOGLE_ADS_ID", "")
    GOOGLE_SITE_VERIFICATION = os.getenv("GOOGLE_SITE_VERIFICATION", "")

    # --------------------------------------------------
    # Social & Tracking
    # --------------------------------------------------
    FACEBOOK_PIXEL_ID = os.getenv("FACEBOOK_PIXEL_ID", "")
    LINKEDIN_INSIGHT_ID = os.getenv("LINKEDIN_INSIGHT_ID", "")
    HOTJAR_ID = os.getenv("HOTJAR_ID", "")
    CLARITY_ID = os.getenv("CLARITY_ID", "")

    # --------------------------------------------------
    # CRM (HubSpot)
    # --------------------------------------------------
    HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY", "")

    # --------------------------------------------------
    # Multilingual and SEO
    # --------------------------------------------------
    DEFAULT_LANGUAGE = "en"
    SUPPORTED_LANGUAGES = ["en", "es", "pt"]

    # --------------------------------------------------
    # AI and Automation Scripts
    # --------------------------------------------------
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GMB_API_KEY = os.getenv("GMB_API_KEY", "")
    AUTO_BACKU_
