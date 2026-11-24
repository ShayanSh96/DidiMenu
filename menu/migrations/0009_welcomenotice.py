from django.db import migrations, models

def seed(apps, schema_editor):
    apps.get_model("menu", "WelcomeNotice").objects.get_or_create(pk=1)

class Migration(migrations.Migration):
    dependencies = [("menu", "0008_menuitem_is_archived")]
    operations = [
        migrations.CreateModel(
            name="WelcomeNotice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, default="به فضای دی‌دی خوش آمدید!", verbose_name="عنوان")),
                ("body", models.TextField(default="خوشحالیم که میزبان شما هستیم. برای اینکه تجربه‌ای آرام، منظم و دلنشین برای همه مهمانان عزیزمان فراهم شود، لطفاً به نکات زیر توجه فرمایید:\n\nموسیقی در طبقه پایین با صدای بالاتری پخش می‌شود و طبقه بالا فضای آرام‌تر با صدای موسیقی کمتری دارد.\n\nمدت استفاده از میزها برای کافی‌شاپ، از زمان ثبت سفارش ۶۰ دقیقه و برای سرو شام ۷۵ دقیقه در نظر گرفته شده است.\n\nدر روزهای پر مهمان دی‌دی ، از ساعت ۲۰:۳۰ پذیرش سفارش شامل شام به همراه سفارش کافی‌شاپ خواهد بود.\n\nبرای نظم بهتر در میزبانی از شما عزیزان خواهشمندیم در ساعت اعلام‌شده برای رزرو حضور داشته باشید.\n\nدر صورت تأخیر بیش از ۱۵ دقیقه، رزرو به‌صورت خودکار لغو خواهد شد.\n\nاز همراهی و درک شما سپاسگزاریم و امیدواریم لحظات خوشی را در دی‌دی تجربه کنید.", verbose_name="متن اطلاعیه")),
                ("button_label", models.CharField(max_length=100, default="متوجه شدم، ورود به سایت", verbose_name="متن دکمه")),
                ("is_active", models.BooleanField(default=True, verbose_name="فعال")),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name": "اطلاعیه ورود به سایت", "verbose_name_plural": "اطلاعیه ورود به سایت"},
        ),
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
