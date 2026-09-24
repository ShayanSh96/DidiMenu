from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0004_menuitem_price_on_request"),
    ]

    operations = [
        migrations.CreateModel(
            name="AvailabilityMenuItem",
            fields=[],
            options={
                "verbose_name": "موجودی محصول",
                "verbose_name_plural": "مدیریت موجودی محصولات",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("menu.menuitem",),
        ),
    ]
