from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html

from .models import AvailabilityMenuItem, Category, MenuItem


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
        "arabic_name",
        "category",
        "price",
        "price_on_request",
        "is_available",
        "is_featured",
        "sort_order",
    )
    list_filter = ("category", "price_on_request", "is_available", "is_featured")
    list_editable = (
        "english_name",
        "arabic_name",
        "price",
        "price_on_request",
        "is_available",
        "is_featured",
        "sort_order",
    )
    search_fields = (
        "name",
        "english_name",
        "arabic_name",
        "description",
        "description_en",
        "description_ar",
    )
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("category",)
    ordering = ("category__sort_order", "sort_order", "name")
    fieldsets = (
        ("اطلاعات اصلی", {
            "fields": (
                "category",
                "name",
                "english_name",
                "arabic_name",
                "slug",
                "price",
                "price_on_request",
                "image",
            )
        }),
        ("توضیحات سه زبانه", {
            "fields": ("description", "description_en", "description_ar")
        }),
        ("وضعیت نمایش", {
            "fields": ("is_available", "is_featured", "sort_order")
        }),
    )


@admin.register(AvailabilityMenuItem)
class AvailabilityMenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "availability_status", "availability_action")
    list_filter = ("category", "is_available")
    search_fields = ("name", "english_name", "arabic_name")
    ordering = ("category__sort_order", "sort_order", "name")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_active and request.user.is_staff

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:object_id>/toggle-availability/",
                self.admin_site.admin_view(self.toggle_availability),
                name="menu_availability_toggle",
            ),
        ]
        return custom_urls + urls

    @admin.display(description="وضعیت")
    def availability_status(self, obj):
        if obj.is_available:
            return format_html('<strong style="color:{}">{}</strong>', "#198754", "موجود")
        return format_html('<strong style="color:{}">{}</strong>', "#dc3545", "ناموجود")

    @admin.display(description="تغییر موجودی")
    def availability_action(self, obj):
        url = reverse("admin:menu_availability_toggle", args=[obj.pk])
        label = "ناموجود کن" if obj.is_available else "موجود کن"
        return format_html(
            '<a class="button" href="{}" style="white-space:nowrap">{}</a>',
            url,
            label,
        )

    def toggle_availability(self, request, object_id):
        if not self.has_change_permission(request):
            raise PermissionDenied
        item = self.get_object(request, object_id)
        if item is None:
            raise PermissionDenied
        item.is_available = not item.is_available
        item.save(update_fields=["is_available"])
        return HttpResponseRedirect(reverse("admin:menu_availabilitymenuitem_changelist"))

    def get_readonly_fields(self, request, obj=None):
        return ("name", "english_name", "arabic_name", "category", "is_available")

    def get_fields(self, request, obj=None):
        return ("name", "english_name", "arabic_name", "category", "is_available")

    def save_model(self, request, obj, form, change):
        if change:
            old = MenuItem.objects.get(pk=obj.pk)
            obj.category = old.category
            obj.name = old.name
            obj.english_name = old.english_name
            obj.arabic_name = old.arabic_name
            obj.slug = old.slug
            obj.description = old.description
            obj.description_en = old.description_en
            obj.description_ar = old.description_ar
            obj.price = old.price
            obj.price_on_request = old.price_on_request
            obj.image = old.image
            obj.is_featured = old.is_featured
            obj.sort_order = old.sort_order
        super().save_model(request, obj, form, change)


admin.site.site_header = "DIDI Menu Admin"
admin.site.site_title = "DIDI Menu"
admin.site.index_title = "مدیریت منو"
