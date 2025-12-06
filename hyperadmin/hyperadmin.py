import logging
from django.contrib.admin import AdminSite
from django.urls import NoReverseMatch, path, reverse
from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.urls import reverse

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
        self._extra_views = [
            path(
                "settings/",
                self.admin_view(self.settings_view),
                name="settings",
            ),
            # TODO: add a legit versioned admin api with openapi spport
            path(
                "global-search",
                self.admin_view(self.global_search_api),
                name="global_search_api",
            ),
        ]  # register_view()
        self._extra_sidebar_modules = []  # add_module()
        self._realms = []
        self._global_search_providers: list = []

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

    def register_realm(
        self,
        name: str,
        *,
        context_factory=None,
        sidebar_template: str | None = None,
        topbar_template: str | None = None,
        search_providers: list | None = None,
        label: str | None = None,
        order: int = 100,
    ):
        """
        Register a 'realm' - a named variant of the admin with its own
        sidebar/topbar templates, extra context and search providers.
        """
        if name in self._realms:
            raise ValueError(f"Realm {name!r} is already registered")

        self._realms[name] = {
            "name": name,
            "label": label or name.title(),
            "context_factory": context_factory,
            "sidebar_template": sidebar_template,
            "topbar_template": topbar_template,
            "search_providers": list(search_providers or []),
            "order": order,
        }

    def register_global_search(self, provider):
        """
        provider(request, query) -> list[dict]

        Each dict should have at least:
        {
          "source": "articles",   # arbitrary string
          "label": "Article title",
          "url": "/articles/slug/",
          "description": "Optional text",
        }
        """
        self.global_search_providers.append(provider)

    # Filter URLs -> absolute URL + skipping missing reverses
    def _resolve_module_items(self, module, request):
        items = []
        module_id = module.get("id")

        for item in module.get("items", []):
            url_name = item.get("url_name")

            if not url_name:
                logger.warning(
                    "[Hyperadmin] item missing url_name (module_id=%r, item=%r, user=%r)",
                    module_id,
                    item,
                    request.user,
                )
                continue

            try:
                url = reverse(url_name)
            except NoReverseMatch as exc:
                logger.warning(
                    "[Hyperadmin] cannot reverse url_name=%r in module_id=%r: %s",
                    url_name,
                    module_id,
                    exc,
                )
                continue

            items.append(
                {
                    "label": item.get("label", url_name),
                    "url": url,
                }
            )

        return items

    def get_extra_sidebar_modules(self, request):
        """
        Final list of modules shown in the sidebar.
        """
        resolved = []
        for module in self._extra_sidebar_modules:
            items = self._resolve_module_items(module, request)
            if items:
                resolved.append(
                    {
                        "id": module["id"],
                        "title": module.get("title"),
                        "items": items,
                    }
                )

        return resolved

    # Inject modules into admin context
    def each_context(self, request):
        ctx = super().each_context(request)
        ctx["extra_modules"] = self.get_extra_sidebar_modules(request)
        return ctx

    def settings_view(self, request):
        """
        "Settings" page inside admin, using HyperadminSite context.
        """

        try:
            docsroot = reverse("django-admindocs-docroot")
        except NoReverseMatch:
            docsroot = None

        try:
            profile_url = reverse("admin:auth_user_change", args=[request.user.pk])
        except NoReverseMatch:
            profile_url = None

        context = dict(
            self.each_context(request),
            title=("Settings"),
            docsroot=docsroot,
            profile_url=profile_url,
        )

        return TemplateResponse(
            request,
            "hyperadmin/settings.html",
            context,
        )

    def _get_object_content(self, obj):
        """
        Try to extract a reasonable 'content' snippet for an object.
        Adjust this to your needs (add fields, etc.).
        """
        candidate_fields = ["description", "content", "body", "text"]
        for field in candidate_fields:
            if hasattr(obj, field):
                val = getattr(obj, field)
                if isinstance(val, str) and val.strip():
                    return val[:500]
        return str(obj)

    def global_search_api(self, request):
        """
        JSON global search endpoint.

        Expects ?query=...
        Returns:
            {
            "results": [
                {
                "title": "...",
                "content": "...",
                "url": "/hyperadmin/admin/app/model/pk/change/"
                },
                ...
            ]
            }
        """
        query = (request.GET.get("query") or "").strip()
        results = []

        if not query:
            return JsonResponse({"results": []})

        # 1) Search in all admin-registered models with search_fields
        for model, model_admin in self._registry.items():
            search_fields = model_admin.get_search_fields(request)
            if not search_fields:
                continue

            qs = model_admin.get_queryset(request)
            qs, use_distinct = model_admin.get_search_results(request, qs, query)
            if use_distinct:
                qs = qs.distinct()

            if not qs.exists():
                continue

            opts = model._meta
            change_url_name = f"admin:{opts.app_label}_{opts.model_name}_change"

            for obj in qs[:5]:  # limit per model
                title = opts.object_name
                content = self._get_object_content(obj)
                url = reverse(change_url_name, args=[obj.pk])

                results.append(
                    {
                        "title": title,
                        "content": content,
                        "url": url,
                    }
                )

        # 2) Extra providers for non-admin search (optional)
        for provider in getattr(self, "_global_search_providers", []):
            try:
                extra = provider(request, query) or []
            except Exception:
                extra = []

            for item in extra:
                norm = {
                    "title": item.get("title", ""),
                    "content": item.get("content", "") or item.get("description", ""),
                    "url": item.get("url", ""),
                }
                results.append(norm)

        # optional global cap
        results = results[:200]

        return JsonResponse({"results": results})
