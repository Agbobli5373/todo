from django.shortcuts import render
from cat.domain import services

from django.views.decorators.http import require_GET


@require_GET
async def index(request):
    cat = await services.get_cat()
    context = {"cat": cat}
    if request.htmx:
        return render(request, "cat/partials/_index.html", context)

    return render(request, "cat/index.html", context)
