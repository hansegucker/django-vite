from contextlib import suppress

from django.apps import AppConfig
from django.core.checks import Warning, register

from .core.exceptions import DjangoViteManifestError
from .templatetags.django_vite import DjangoViteAssetLoader


class DjangoViteAppConfig(AppConfig):
    name = "django_vite"
    verbose_name = "Django Vite"

    def ready(self) -> None:
        with suppress(DjangoViteManifestError):
            # Create Loader instance at startup to prevent threading problems,
            # but do not crash while doing so.
            DjangoViteAssetLoader.instance()


@register
def check_loader_instance(**kwargs):
    """Raise a warning during startup when instance retrieval fails."""

    try:
        # Make Loader instance at startup to prevent threading problems
        DjangoViteAssetLoader.instance()
        return []
    except DjangoViteManifestError as exception:
        return [
            Warning(
                exception,
                id="DJANGO_VITE",
                hint=(
                    "Make sure you have generated a manifest file, "
                    "and that the DJANGO_VITE_MANIFEST_PATH points "
                    "to the correct location."
                ),
            )
        ]
