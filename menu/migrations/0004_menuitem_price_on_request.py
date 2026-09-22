from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0003_menuitem_arabic_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="price_on_request",
            field=models.BooleanField(
                default=False,
                help_text="اگر فعال باشد، به جای قیمت عبارت «با هماهنگی / رزرو قبلی» نمایش داده می‌شود.",
                verbose_name="قیمت با هماهنگی / رزرو قبلی",
            ),
        ),
    ]
