from django.shortcuts import render
from django.shortcuts import render
from django.db.models import Prefetch

from .models import Transaction, OwningSubject, Project, AssetSource, Unit


def transaction_list(request):
    """
    Very simple view that lists transactions, optionally filtered
    by subject or project via query params:
    ?subject_id=1&project_id=3
    """
    qs = Transaction.objects.select_related(
        "subject",
        "unit",
        "project",
        "from_asset_source",
        "to_asset_source",
    )

    subject_id = request.GET.get("subject_id")
    project_id = request.GET.get("project_id")

    if subject_id:
        qs = qs.filter(subject_id=subject_id)

    if project_id:
        qs = qs.filter(project_id=project_id)

    qs = qs.order_by("-occurred_at", "-id")

    context = {
        "transactions": qs,
        "subjects": OwningSubject.objects.all().order_by("name"),
        "projects": Project.objects.all().order_by("name"),
    }
    return render(request, "finance/transaction_list.html", context)
