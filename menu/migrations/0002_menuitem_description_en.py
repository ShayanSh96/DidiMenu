from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="description_en",
            field=models.TextField(blank=True, verbose_name="توضیحات انگلیسی"),
        ),
        migrations.AlterField(
            model_name="menuitem",
            name="description",
            field=models.TextField(blank=True, verbose_name="توضیحات فارسی"),
        ),
    ]
