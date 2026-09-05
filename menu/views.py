from django.shortcuts import get_object_or_404, render

from .models import Category, MenuItem


CATEGORY_NAMES_EN = {
    "breakfast": "Breakfast",
    "iranian-breakfast": "Iranian Breakfast",
    "hot-coffee": "Hot Coffee",
    "cold-coffee": "Cold Coffee",
    "hot-drinks": "Hot Drinks",
    "tea-herbal": "Tea & Herbal Drinks",
    "mocktails": "Mocktails",
    "bakery": "Bakery",
    "desserts": "Desserts",
    "natural-drinks": "Natural Drinks",
    "smoothies": "Smoothies",
    "milkshakes": "Milkshakes",
    "fizzy-bar": "Fizzy Bar",
    "bar-addons": "Bar Add-ons",
    "brewed-coffee": "Brewed Coffee",
    "appetizers": "Appetizers",
    "pizza-xl": "Pizza XL",
    "pizza-large": "Pizza Large",
    "pasta": "Pasta",
    "steak": "Steak",
    "king-burger": "King Burger",
    "burger-180": "180g Burger",
    "burger-addons": "Burger Add-ons",
    "plates": "Plates",
}


def _language_context(request):
    requested = request.GET.get("lang")
    if requested in {"fa", "en"}:
        request.session["site_language"] = requested

    lang = request.session.get("site_language", "fa")
    if lang not in {"fa", "en"}:
        lang = "fa"

    params = request.GET.copy()
    params["lang"] = "en" if lang == "fa" else "fa"
    query = params.urlencode()

    return {
        "lang": lang,
        "is_en": lang == "en",
        "switch_lang": "en" if lang == "fa" else "fa",
        "switch_url": f"{request.path}?{query}" if query else request.path,
    }


def _localize_categories(categories, lang):
    for category in categories:
        category.display_name = (
            CATEGORY_NAMES_EN.get(category.slug, category.name)
            if lang == "en"
            else category.name
        )
    return categories


def _localize_items(items, lang):
    for item in items:
        if lang == "en":
            item.display_name = item.english_name or item.name
            item.secondary_name = ""
            item.display_description = ""
        else:
            item.display_name = item.name
            item.secondary_name = item.english_name
            item.display_description = item.description
    return items


def welcome(request):
    return render(request, "menu/welcome.html", _language_context(request))


def story(request):
    return render(request, "menu/story.html", _language_context(request))


def family(request):
    return render(request, "menu/family.html", _language_context(request))


def menu_home(request):
    ctx = _language_context(request)
    lang = ctx["lang"]

    categories = list(Category.objects.filter(is_active=True))
    _localize_categories(categories, lang)

    selected_slug = request.GET.get("category")

    if not selected_slug:
        ctx["categories"] = categories
        return render(request, "menu/categories.html", ctx)

    selected_category = next(
        (category for category in categories if category.slug == selected_slug),
        None,
    )

    if selected_category is None:
        ctx["categories"] = categories
        return render(request, "menu/categories.html", ctx)

    items = list(
        MenuItem.objects.filter(category=selected_category).order_by(
            "sort_order", "name"
        )
    )
    _localize_items(items, lang)

    ctx.update(
        {
            "categories": categories,
            "selected_category": selected_category,
            "items": items,
        }
    )
    return render(request, "menu/home.html", ctx)


def item_detail(request, slug):
    ctx = _language_context(request)
    item = get_object_or_404(MenuItem.objects.select_related("category"), slug=slug)

    if ctx["lang"] == "en":
        item.display_name = item.english_name or item.name
        item.secondary_name = ""
        item.display_description = ""
    else:
        item.display_name = item.name
        item.secondary_name = item.english_name
        item.display_description = item.description

    item.category.display_name = (
        CATEGORY_NAMES_EN.get(item.category.slug, item.category.name)
        if ctx["lang"] == "en"
        else item.category.name
    )

    ctx["item"] = item
    return render(request, "menu/item_detail.html", ctx)
