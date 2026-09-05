from django.core.management.base import BaseCommand
from menu.models import MenuItem

CORRECTIONS = {
    "sausage-fried-egg": "Sausage Fried Egg",
    "egg-fried-ghormeh": "Fried Egg with Ghormeh",
    "airish-beer": "Irish Beer",
    "soda-lemon": "Lemon Soda",
    "xl-parmigiano-pizza": "Bacon Cream Pizza",
    "king-spicy-camembert-burger": "Buffalo Camembert Burger",
    "180-spicy-camembert-burger": "Buffalo Camembert Burger",
    "180-halloumi-mushroom-burger": "Halloumi Mushroom Burger",
    "blaze-butter-steaks": "Blaze & Butter Steak",
}


class Command(BaseCommand):
    help = "Correct verified English menu item names."

    def handle(self, *args, **options):
        changed = 0
        missing = []

        for slug, new_name in CORRECTIONS.items():
            try:
                item = MenuItem.objects.get(slug=slug)
            except MenuItem.DoesNotExist:
                missing.append(slug)
                continue

            old_name = item.english_name or ""
            if old_name == new_name:
                self.stdout.write(f"OK: {slug} -> {new_name}")
                continue

            item.english_name = new_name
            item.save(update_fields=["english_name"])
            changed += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"CHANGED: {slug}: {old_name!r} -> {new_name!r}"
                )
            )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Updated {changed} item(s)."))

        if missing:
            self.stdout.write(
                self.style.WARNING(
                    "Missing slugs: " + ", ".join(missing)
                )
            )
