from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=140, unique=True, verbose_name="اسلاگ")
    image = models.ImageField(
        upload_to="menu/categories/",
        blank=True,
        null=True,
        verbose_name="تصویر دسته‌بندی",
    )
    sort_order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="items",
        verbose_name="دسته‌بندی",
    )
    name = models.CharField(max_length=160, verbose_name="نام محصول")
    english_name = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="نام انگلیسی",
    )
    slug = models.SlugField(max_length=180, unique=True, verbose_name="اسلاگ")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    price = models.PositiveIntegerField(verbose_name="قیمت")
    image = models.ImageField(
        upload_to="menu/items/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="تصویر",
    )
    is_available = models.BooleanField(default=True, verbose_name="موجود")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category__sort_order", "sort_order", "name"]
        verbose_name = "محصول منو"
        verbose_name_plural = "محصولات منو"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("menu:item_detail", kwargs={"slug": self.slug})
