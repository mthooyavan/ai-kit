# pylint: disable=import-outside-toplevel, unused-import

from logging import getLogger

from django import apps

from ai_kit import __version__

logger = getLogger(__name__)


class AppConfig(apps.AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "ai_kit"
    initialized = False

    @classmethod
    def initialize(cls):
        """
        Initialize Axes logging and show version information.

        This method is re-entrant and can be called multiple times.
        It displays version information exactly once at application startup.
        """

        if cls.initialized:
            return
        cls.initialized = True

        # Only import settings, checks, and signals one time after Django has been initialized
        from ai_kit.conf import settings  # isort:skip
        from ai_kit import checks, signals

    def ready(self):
        self.initialize()
