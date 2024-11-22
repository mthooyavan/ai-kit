from django.db import models

from ai_kit.utils.enums import LLM_PROVIDERS


class LLMModel(models.Model):
    version_name = models.CharField(
        max_length=100, help_text="The version name of the model"
    )
    display_name = models.CharField(
        max_length=100, help_text="The display name of the model"
    )
    provider = models.CharField(
        max_length=20, choices=LLM_PROVIDERS, help_text="The provider of the model"
    )

    is_enabled = models.BooleanField(
        default=True, help_text="Whether the model is enabled"
    )
    is_multimodal = models.BooleanField(
        default=False, help_text="Whether the model supports images"
    )
    is_function_calling_supported = models.BooleanField(
        default=False, help_text="Whether the model supports function calling"
    )
    description = models.TextField(blank=True, help_text="The description of the model")
    settings = models.JSONField(
        default=dict, blank=True, null=True, help_text="The settings of the model"
    )

    class Meta:
        verbose_name = "LLM Model"
        verbose_name_plural = "LLM Models"
        ordering = ["provider", "display_name", "version_name"]
        unique_together = [("provider", "version_name")]

    def __str__(self):
        return f"{self.provider} - {self.display_name} ({self.version_name})"
