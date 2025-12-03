import logging
from django.contrib.admin import AdminSite
from django.urls import NoReverseMatch, path, reverse

logger = logging.getLogger(__name__)


class HyperadminSite(AdminSite):
    """
    A lightweight extension of Django AdminSite with:
    - extra views (custom URLs added by apps)
    - extra modules (sidebar/menus)
    """

    site_header = "Hyperadmin"
    site_title = "Hyperadmin"

    #
    # --- CUSTOMIZABLE HOOK STORAGE ---
    #
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._extra_views = []      # register_view()
        self._extra_sidebar_modules = []    # add_module()
        self._domains = []

    # ---------------------------------------------------------
    #  HOOK #1: EXTRA ADMIN VIEWS (custom URLs)
    # ---------------------------------------------------------

    def register_view(self, route: str, view, name: str):
        """
        Register a custom view accessible under this admin site.
        """
        self._extra_views.append(path(route, self.admin_view(view), name=name))

    # Include extra views BEFORE stock admin views.
    def get_urls(self):
        return self._extra_views + super().get_urls()

    # ---------------------------------------------------------
    #  HOOK #2: SIDEBAR MODULES
    # ---------------------------------------------------------

    def add_sidebar_modules(self, module_dict: dict):
        """
        Add a sidebar item *from external apps*.
        Format:
            {"id": "...", "title": "...", "items": [{"label": "...", "url_name": "..."}]}
        """
        self._extra_sidebar_modules.append(module_dict)

    def add_domain(self, domain):
        self._domains.append(domain)

    # Filter URLs -> absolute URL + skipping missing reverses
    def _resolve_module_items(self, module, request):
        items = []
        module_id = module.get("id")

        for item in module.get("items", []):
            url_name = item.get("url_name")

            if not url_name:
                logger.warning(
                    "[Hyperadmin] item missing url_name (module_id=%r, item=%r, user=%r)",
                    module_id, item, request.user,
                )
                continue

            try:
                url = reverse(url_name)
            except NoReverseMatch as exc:
                logger.warning(
                    "[Hyperadmin] cannot reverse url_name=%r in module_id=%r: %s",
                    url_name, module_id, exc,
                )
                continue

            items.append({
                "label": item.get("label", url_name),
                "url": url,
            })

        return items

    def get_extra_sidebar_modules(self, request):
        """
        Final list of modules shown in the sidebar.
        """
        resolved = []
        for module in self._extra_sidebar_modules:
            items = self._resolve_module_items(module, request)
            if items:
                resolved.append({
                    "id": module["id"],
                    "title": module.get("title"),
                    "items": items,
                })

        return resolved

    # Inject modules into admin context
    def each_context(self, request):
        ctx = super().each_context(request)
        ctx["extra_modules"] = self.get_extra_sidebar_modules(request)
        return ctx
