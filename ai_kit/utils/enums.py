from django.utils.translation import gettext_lazy as _
from model_utils import Choices

LLM_PROVIDERS = Choices(
    ("openai", _("OpenAI")),
    ("bedrock", _("AWS Bedrock")),
)
