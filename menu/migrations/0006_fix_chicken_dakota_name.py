from django.db import migrations


def fix_chicken_dakota_name(apps, schema_editor):
    MenuItem = apps.get_model("menu", "MenuItem")
    MenuItem.objects.filter(slug="dakota-chicken").update(name="چیکن داکوتا")


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0005_availabilitymenuitem"),
    ]

    operations = [
        migrations.RunPython(fix_chicken_dakota_name, migrations.RunPython.noop),
    ]
