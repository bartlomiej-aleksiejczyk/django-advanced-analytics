from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from hyperadmin.hyperadmin import HyperadminSite


hyperadmin = HyperadminSite(name="admin")

# Queues for lazy registration
queued_autoreg_apps = []
queued_views = []
queued_actions = []

# def autoregister_app_models(app_label: str, site: HyperadminSite):
#     app_config = apps.get_app_config(app_label)
#     for model in app_config.get_models():
#         try:
#             site.register(model)
#         except AlreadyRegistered:
#             pass


# def register_hyperadmin():
#     # called from AppConfig.ready()
#     autoregister_app_models("auth", hyperadmin)
#     autoregister_app_models("django_q", hyperadmin)

#     # actions must also be added inside ready()
#     def export_everything(modeladmin, request, queryset):
#         pass

#     export_everything.short_description = "Export all data"
#     hyperadmin.add_action(export_everything, name="export_everything")
