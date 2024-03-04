from django.shortcuts import render
from shopping.domain import services
from django.views.decorators.http import require_POST, require_GET
from shopping import forms


@require_GET
async def index(request):
    items = await services.get_all_items()
    context = {"items": items}

    if request.htmx:
        return render(request, "shopping/partials/_index.html", context)

    return render(request, "shopping/index.html", context)


@require_POST
async def create_new_item(request):
    form = forms.NewItemForm(request.POST)
    if form.is_valid():
        await services.add_new_item(form.cleaned_data["name"])
    else:
        raise Exception("unhandled")

    items = await services.get_all_items()
    context = {"items": items}
    if request.htmx:
        return render(request, "shopping/partials/_items.html", context)

    return render(request, "shopping/index.html", context)


@require_POST
async def complete_item(request):
    form = forms.ItemIDForm(request.POST)
    if not form.is_valid():
        raise Exception("unhandled")

    await services.complete_item(form.cleaned_data["item_id"])

    items = await services.get_all_items()
    context = {"items": items}
    if request.htmx:
        return render(request, "shopping/partials/_items.html", context)

    return render(request, "shopping/index.html", context)


@require_POST
async def undo_item(request):
    form = forms.ItemIDForm(request.POST)
    if not form.is_valid():
        raise Exception("unhandled")

    await services.undo_item(form.cleaned_data["item_id"])

    items = await services.get_all_items()
    context = {"items": items}
    if request.htmx:
        return render(request, "shopping/partials/_items.html", context)

    return render(request, "shopping/index.html", context)
