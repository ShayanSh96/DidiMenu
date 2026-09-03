from django.shortcuts import get_object_or_404, render

from .models import Category, MenuItem


def welcome(request):
    return render(request, "menu/welcome.html")


def story(request):
    return render(request, "menu/story.html")


def family(request):
    return render(request, "menu/under_construction.html", {"page_title": "خانواده‌ی دیدی"})


def menu_home(request):
    categories = Category.objects.filter(is_active=True)
    selected_slug = request.GET.get("category")

    if not selected_slug:
        return render(request, "menu/categories.html", {"categories": categories})

    selected_category = categories.filter(slug=selected_slug).first()

    if selected_category is None:
        return render(request, "menu/categories.html", {"categories": categories})

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
