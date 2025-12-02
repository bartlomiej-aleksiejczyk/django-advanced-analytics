from django.apps import AppConfig


from django.apps import AppConfig

class HyperAdminConfig(AppConfig):
    name = "hyperadmin"

    def ready(self):
        from django.apps import apps
        from django.contrib.admin.sites import AlreadyRegistered

        from .admin import hyperadmin, queued_autoreg_apps, queued_views, queued_actions

        #
        # 1. Autoregister models
        #
        for app_label in queued_autoreg_apps:
            app_config = apps.get_app_config(app_label)
            for model in app_config.get_models():
                try:
                    hyperadmin.register(model)
                except AlreadyRegistered:
                    pass

        #
        # 2. Extra views
        #
        for pattern, view, name in queued_views:
            hyperadmin.register_view(pattern, view, name=name)

        #
        # 3. Actions
        #
        for action, name in queued_actions:
            hyperadmin.add_action(action, name=name)
