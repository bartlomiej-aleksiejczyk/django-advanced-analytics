from django.apps import AppConfig


class PrototypeSetupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prototype_setup'
    verbose_name = "Customized Settings"

    # noinspection PyUnresolvedReferences
    def ready(self):
        from . import signals