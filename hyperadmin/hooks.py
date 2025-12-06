from .admin import (
    queued_autoreg_sidebar_modules,
    queued_autoreg_apps,
    queued_views,
    queued_actions,
    queued_realms,
)


def register_admin_autoreg(app_label):
    queued_autoreg_apps.append(app_label)


def register_admin_sidebar_modules(module):
    queued_autoreg_sidebar_modules.append(module)


def register_admin_view(pattern, view_factory, name=None):
    """
    view_factory: callable(admin_site) -> view(request)
    """
    queued_views.append((pattern, view_factory, name))


def register_admin_action(action, name=None):
    queued_actions.append((action, name))


def register_admin_realm(realm):
    queued_realms.append((realm))
