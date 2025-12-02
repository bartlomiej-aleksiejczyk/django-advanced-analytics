from django.apps import AppConfig
from hyperadmin.admin import hyperadmin
from django.template.response import TemplateResponse
from hyperadmin.hooks import register_admin_action, register_admin_view

def system_dashboard_view(request):
    context = {"title": "System dashboard"}
    return TemplateResponse(request, "admin/system_dashboard.html", context)

def export_everything(modeladmin, request, queryset):
    pass

class NotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notes'
    def ready(self):
        register_admin_view(
            "dashboard/",
            system_dashboard_view,
            name="dashboard"
        )
    register_admin_action(export_everything, name="export_all")
