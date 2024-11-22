from django.conf import settings

from ai_kit.models import LLMModel


class ModelRegistry:

    def initialize(self):
        try:
            registered_models = settings.AI_KIT_MODEL_REGISTRY
        except AttributeError:
            return

        for registered_model in registered_models:
            model, created = LLMModel.objects.get_or_create(
                provider=registered_model["provider_name"],
                version_name=registered_model["version_name"],
                defaults={
                    "display_name": registered_model["display_name"],
                },
            )
            if created:
                print("New LLM Model has been created: ", model)
            else:
                print("Selected LLM Model already exists: ", model)
