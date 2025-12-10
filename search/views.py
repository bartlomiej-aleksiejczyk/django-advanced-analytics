from django.http import JsonResponse

from search.providers import provider_registry


def global_search_api(request) -> JsonResponse:
        """
        JSON global search endpoint.

        Expects ?query=...
        Returns:
            {
            "results": [
                {
                "title": "...",
                "content": "...",
                "url": "/hyperdossier/admin/app/model/pk/change/"
                },
                ...
            ]
            }
        """
        query = (request.GET.get("query") or "").strip()
        results = []

        if not query:
            return JsonResponse({"results": []})

        for provider in provider_registry:
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

        results = results[:200]

        return JsonResponse({"results": results})
