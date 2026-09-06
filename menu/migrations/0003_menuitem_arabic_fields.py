from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0002_menuitem_description_en"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="arabic_name",
            field=models.CharField(blank=True, max_length=160, verbose_name="نام عربی"),
        ),
        migrations.AddField(
            model_name="menuitem",
            name="description_ar",
            field=models.TextField(blank=True, verbose_name="توضیحات عربی"),
        ),
    ]
