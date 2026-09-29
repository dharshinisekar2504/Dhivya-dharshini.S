import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = BASE_DIR / "static"
PANELS_DIR = STATIC_DIR / "panels"
EXPORTS_DIR = STATIC_DIR / "exports"

PANELS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

IMAGE_PROVIDER = os.getenv("IMAGE_PROVIDER", "placeholder").lower()

IMAGE_MODEL = os.getenv(
    "IMAGE_MODEL",
    "stable-diffusion-v1-5/stable-diffusion-v1-5"
)

IMAGE_STEPS = int(os.getenv("IMAGE_STEPS", "20"))
IMAGE_WIDTH = int(os.getenv("IMAGE_WIDTH", "512"))
IMAGE_HEIGHT = int(os.getenv("IMAGE_HEIGHT", "512"))

MAX_PANELS = 5