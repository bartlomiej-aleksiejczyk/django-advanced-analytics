from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from hyperadmin.hyperadmin import HyperadminSite


hyperadmin = HyperadminSite(name="admin")

queued_autoreg_sidebar_modules = []
queued_autoreg_apps = []
queued_views = []
queued_actions = []
queued_realms = []
