from django.shortcuts import get_object_or_404, render

from .models import Category, MenuItem


def menu_home(request):
    categories = Category.objects.filter(is_active=True)

    selected_slug = request.GET.get("category")
    selected_category = None

    if selected_slug:
        selected_category = categories.filter(slug=selected_slug).first()

    if selected_category is None:
        selected_category = categories.first()

    items = MenuItem.objects.none()
    if selected_category:
        items = MenuItem.objects.filter(category=selected_category).order_by(
            "sort_order", "name"
        )

    context = {
        "categories": categories,
        "selected_category": selected_category,
        "items": items,
    }
    return render(request, "menu/home.html", context)


def item_detail(request, slug):
    item = get_object_or_404(MenuItem.objects.select_related("category"), slug=slug)
    return render(request, "menu/item_detail.html", {"item": item})
