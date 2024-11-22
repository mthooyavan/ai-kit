from django.core.signals import setting_changed
from django.dispatch import receiver

from ai_kit.registry import ModelRegistry


@receiver(setting_changed)
def handle_setting_changed(
    sender, setting, value, enter, **kwargs
):  # pylint: disable=unused-argument
    """
    Reinitialize handler implementation if a relevant setting changes
    in e.g. application reconfiguration or during testing.
    """
    if setting == "AI_KIT_MODEL_REGISTRY":
        ModelRegistry.initialize()
