import os
from dotenv import load_dotenv

load_dotenv()

WP_URL: str = os.getenv("WP_URL", "http://keiji-bengo-navi.local")
WP_USER: str = os.getenv("WP_USER", "admin")
WP_APP_PASSWORD: str = os.getenv("WP_APP_PASSWORD", "")
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
STATIC_EXPORT_DIR: str = os.getenv("STATIC_EXPORT_DIR", "./static-export")
USE_WPCLI: bool = os.getenv("USE_WPCLI", "true").lower() == "true"
