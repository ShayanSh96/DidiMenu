from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0005_availabilitymenuitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="is_coming_soon",
            field=models.BooleanField(default=False, verbose_name="به زودی"),
        ),
    ]
