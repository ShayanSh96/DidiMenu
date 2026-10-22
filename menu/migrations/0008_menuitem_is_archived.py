from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0007_merge_coming_soon"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="is_archived",
            field=models.BooleanField(default=False, verbose_name="آرشیو شده"),
        ),
    ]
