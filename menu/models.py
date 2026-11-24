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
    arabic_name = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="نام عربی",
    )
    slug = models.SlugField(max_length=180, unique=True, verbose_name="اسلاگ")
    description = models.TextField(blank=True, verbose_name="توضیحات فارسی")
    description_en = models.TextField(blank=True, verbose_name="توضیحات انگلیسی")
    description_ar = models.TextField(blank=True, verbose_name="توضیحات عربی")
    price = models.PositiveIntegerField(verbose_name="قیمت")
    price_on_request = models.BooleanField(
        default=False,
        verbose_name="قیمت با هماهنگی / رزرو قبلی",
        help_text="اگر فعال باشد، به جای قیمت عبارت «با هماهنگی / رزرو قبلی» نمایش داده می‌شود.",
    )
    image = models.ImageField(
        upload_to="menu/items/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="تصویر",
    )
    is_available = models.BooleanField(default=True, verbose_name="موجود")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    is_coming_soon = models.BooleanField(default=False, verbose_name="به زودی")
    is_archived = models.BooleanField(default=False, verbose_name="آرشیو شده")
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


class AvailabilityMenuItem(MenuItem):
    class Meta:
        proxy = True
        verbose_name = "موجودی محصول"
        verbose_name_plural = "مدیریت موجودی محصولات"


class WelcomeNotice(models.Model):
    title = models.CharField(max_length=200, default="به فضای دی‌دی خوش آمدید!", verbose_name="عنوان")
    body = models.TextField(default="خوشحالیم که میزبان شما هستیم. برای اینکه تجربه‌ای آرام، منظم و دلنشین برای همه مهمانان عزیزمان فراهم شود، لطفاً به نکات زیر توجه فرمایید:\n\nموسیقی در طبقه پایین با صدای بالاتری پخش می‌شود و طبقه بالا فضای آرام‌تر با صدای موسیقی کمتری دارد.\n\nمدت استفاده از میزها برای کافی‌شاپ، از زمان ثبت سفارش ۶۰ دقیقه و برای سرو شام ۷۵ دقیقه در نظر گرفته شده است.\n\nدر روزهای پر مهمان دی‌دی ، از ساعت ۲۰:۳۰ پذیرش سفارش شامل شام به همراه سفارش کافی‌شاپ خواهد بود.\n\nبرای نظم بهتر در میزبانی از شما عزیزان خواهشمندیم در ساعت اعلام‌شده برای رزرو حضور داشته باشید.\n\nدر صورت تأخیر بیش از ۱۵ دقیقه، رزرو به‌صورت خودکار لغو خواهد شد.\n\nاز همراهی و درک شما سپاسگزاریم و امیدواریم لحظات خوشی را در دی‌دی تجربه کنید.", verbose_name="متن اطلاعیه")
    button_label = models.CharField(max_length=100, default="متوجه شدم، ورود به سایت", verbose_name="متن دکمه")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "اطلاعیه ورود به سایت"
        verbose_name_plural = "اطلاعیه ورود به سایت"

    def __str__(self):
        return self.title
