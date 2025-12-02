from django.apps import AppConfig

from hyperadmin.hooks import register_admin_autoreg


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'
    verbose_name = "Customized Settings"

    def ready(self):
        from . import signals
        register_admin_autoreg("auth")
        register_admin_autoreg("django_q")
