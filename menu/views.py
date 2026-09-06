from django.shortcuts import get_object_or_404, render

from .models import Category, MenuItem


CATEGORY_NAMES_EN = {
    "breakfast": "Breakfast", "iranian-breakfast": "Iranian Breakfast", "hot-coffee": "Hot Coffee",
    "cold-coffee": "Cold Coffee", "hot-drinks": "Hot Drinks", "tea-herbal": "Tea & Herbal Drinks",
    "mocktails": "Mocktails", "bakery": "Bakery", "desserts": "Desserts", "natural-drinks": "Natural Drinks",
    "smoothies": "Smoothies", "milkshakes": "Milkshakes", "fizzy-bar": "Fizzy Bar", "bar-addons": "Bar Add-ons",
    "brewed-coffee": "Brewed Coffee", "appetizers": "Appetizers", "pizza-xl": "Pizza XL",
    "pizza-large": "Pizza Large", "pasta": "Pasta", "steak": "Steak", "king-burger": "King Burger",
    "burger-180": "180g Burger", "burger-addons": "Burger Add-ons", "plates": "Plates",
}

CATEGORY_NAMES_AR = {
    "breakfast": "الإفطار", "iranian-breakfast": "الإفطار الإيراني", "hot-coffee": "القهوة الساخنة",
    "cold-coffee": "القهوة الباردة", "hot-drinks": "المشروبات الساخنة", "tea-herbal": "الشاي والمشروبات العشبية",
    "mocktails": "موكتيلات", "bakery": "المخبوزات", "desserts": "الحلويات", "natural-drinks": "المشروبات الطبيعية",
    "smoothies": "سموثي", "milkshakes": "ميلك شيك", "fizzy-bar": "المشروبات الغازية", "bar-addons": "إضافات البار",
    "brewed-coffee": "القهوة المقطرة", "appetizers": "المقبلات", "pizza-xl": "بيتزا XL",
    "pizza-large": "بيتزا كبيرة", "pasta": "باستا", "steak": "ستيك", "king-burger": "كينغ برغر",
    "burger-180": "برغر 180 غرام", "burger-addons": "إضافات البرغر", "plates": "الأطباق",
}


def _language_context(request):
    requested = request.GET.get("lang")
    if requested in {"fa", "en", "ar"}:
        request.session["site_language"] = requested

    lang = request.session.get("site_language", "fa")
    if lang not in {"fa", "en", "ar"}:
        lang = "fa"

    def url_for(target_lang):
        params = request.GET.copy()
        params["lang"] = target_lang
        query = params.urlencode()
        return f"{request.path}?{query}" if query else request.path

    return {
        "lang": lang,
        "is_en": lang == "en",
        "is_ar": lang == "ar",
        "lang_url_fa": url_for("fa"),
        "lang_url_en": url_for("en"),
        "lang_url_ar": url_for("ar"),
    }


def _localize_categories(categories, lang):
    for category in categories:
        if lang == "en":
            category.display_name = CATEGORY_NAMES_EN.get(category.slug, category.name)
        elif lang == "ar":
            category.display_name = CATEGORY_NAMES_AR.get(category.slug, category.name)
        else:
            category.display_name = category.name
    return categories


def _localize_items(items, lang):
    for item in items:
        if lang == "en":
            item.display_name = item.english_name or item.name
            item.secondary_name = ""
            item.display_description = item.description_en or item.description
        elif lang == "ar":
            item.display_name = item.arabic_name or item.english_name or item.name
            item.secondary_name = ""
            item.display_description = item.description_ar or item.description_en or item.description
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

    selected_category = next((c for c in categories if c.slug == selected_slug), None)
    if selected_category is None:
        ctx["categories"] = categories
        return render(request, "menu/categories.html", ctx)

    items = list(MenuItem.objects.filter(category=selected_category).order_by("sort_order", "name"))
    _localize_items(items, lang)
    ctx.update({"categories": categories, "selected_category": selected_category, "items": items})
    return render(request, "menu/home.html", ctx)


def item_detail(request, slug):
    ctx = _language_context(request)
    item = get_object_or_404(MenuItem.objects.select_related("category"), slug=slug)
    _localize_items([item], ctx["lang"])
    _localize_categories([item.category], ctx["lang"])
    ctx["item"] = item
    return render(request, "menu/item_detail.html", ctx)
