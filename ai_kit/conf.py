import json
import os

from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

try:
    settings.AI_KIT_MODEL_REGISTRY = json.loads(
        os.environ.get("AI_KIT_MODEL_REGISTRY", "[]")
    )
except json.JSONDecodeError:
    settings.AI_KIT_MODEL_REGISTRY = []
