from django.shortcuts import render
from cat.domain import services

from django.views.decorators.http import require_POST


@require_POST
async def cat_view(request):
    cat = await services.get_cat()
    context = {"cat": cat}
    if request.htmx:
        return render(request, "partials/_cat.html", context)

    return render(request, "index.html", context)
