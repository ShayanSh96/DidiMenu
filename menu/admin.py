from django.contrib import admin

from .models import Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("sort_order", "name")
    fields = ("name", "slug", "image", "sort_order", "is_active")


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "english_name",
        "category",
        "price",
        "is_available",
        "is_featured",
        "sort_order",
    )
    list_filter = ("category", "is_available", "is_featured")
    list_editable = (
        "english_name",
        "price",
        "is_available",
        "is_featured",
        "sort_order",
    )
    search_fields = ("name", "english_name", "description")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("category",)
    ordering = ("category__sort_order", "sort_order", "name")


admin.site.site_header = "DIDI Menu Admin"
admin.site.site_title = "DIDI Menu"
admin.site.index_title = "مدیریت منو"
