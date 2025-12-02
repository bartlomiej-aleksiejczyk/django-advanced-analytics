from .admin import (
    queued_autoreg_apps,
    queued_views,
    queued_actions
)

def register_admin_autoreg(app_label):
    queued_autoreg_apps.append(app_label)

def register_admin_view(pattern, view, name=None):
    queued_views.append((pattern, view, name))

def register_admin_action(action, name=None):
    queued_actions.append((action, name))
