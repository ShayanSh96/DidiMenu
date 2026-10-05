from django.db import migrations


def mark_all_menu_items_unavailable(apps, schema_editor):
    MenuItem = apps.get_model("menu", "MenuItem")
    MenuItem.objects.update(is_available=False)


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0006_fix_chicken_dakota_name"),
    ]

    operations = [
        migrations.RunPython(
            mark_all_menu_items_unavailable,
            migrations.RunPython.noop,
        ),
    ]
