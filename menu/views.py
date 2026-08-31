from django.shortcuts import get_object_or_404, render

from .models import Category, MenuItem


def menu_home(request):
    categories = Category.objects.filter(is_active=True).prefetch_related('items')
    return render(request, 'menu/home.html', {'categories': categories})


def item_detail(request, slug):
    item = get_object_or_404(MenuItem.objects.select_related('category'), slug=slug)
    return render(request, 'menu/item_detail.html', {'item': item})
