import os

import django


def setup_django() -> None:
    """Initialize Django so interactors and ORM are available."""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "social_network.settings.local",
    )
    django.setup()
