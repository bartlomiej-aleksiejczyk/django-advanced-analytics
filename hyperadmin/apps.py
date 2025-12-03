from django.apps import AppConfig


class HyperAdminConfig(AppConfig):
    name = "hyperadmin"

    def ready(self):
        from django.apps import apps
        from django.contrib.admin.sites import AlreadyRegistered
        from .admin import hyperadmin, queued_autoreg_sidebar_modules, queued_autoreg_apps, queued_views, queued_actions, queued_domains

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

        # 1. Autoregister sidebar items
        for module in queued_autoreg_sidebar_modules:
            hyperadmin.add_sidebar_modules(module);

        # 2. Extra views (factories)
        for pattern, view_factory, name in queued_views:
            view = view_factory(hyperadmin)
            hyperadmin.register_view(pattern, view, name=name)

        # 3. Actions
        for action, name in queued_actions:
            hyperadmin.add_action(action, name=name)

        # 5. Domains
        for domain in queued_domains:
            hyperadmin.add_domain(domain)