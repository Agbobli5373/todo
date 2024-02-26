from django.shortcuts import render
from cat.domain import services

from django.views.decorators.http import require_POST


@require_POST
def cat_view(request):
    context = {"cat": services.get_cat()}
    if request.htmx:
        return render(request, "partials/_cat.html", context)

    return render(request, "index.html", context)
