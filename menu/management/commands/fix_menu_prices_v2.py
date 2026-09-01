from copy import deepcopy

from django.core.management.base import BaseCommand

from menu.management.commands.fix_menu_prices import PRICE_GROUPS, normalize
from menu.models import Category, MenuItem


MISSING_BURGER_ADDONS = [
    {
        "name": "سوسیس",
        "english_name": "Sausage",
        "slug": "addon-sausage",
        "price": 180_000,
    },
    {
        "name": "پیاز کاراملی",
        "english_name": "Caramelized Onion",
        "slug": "addon-caramelized-onion",
        "price": 40_000,
    },
    {
        "name": "پیاز بنفش",
        "english_name": "Red Onion",
        "slug": "addon-red-onion",
        "price": 20_000,
    },
]


def verified_price_groups():
    groups = deepcopy(PRICE_GROUPS)
    for category_slug, fixes in groups:
        if category_slug != "burger-addons":
            continue
        for i, (aliases, price) in enumerate(fixes):
            if normalize(aliases[0]) == normalize("Sausage"):
                fixes[i] = (aliases, 180_000)
    return groups


class Command(BaseCommand):
    help = "Apply visually verified DIDI prices and safely add the three missing burger add-ons."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        created = 0
        changed = 0
        correct = 0
        missing = []

        addon_category = Category.objects.filter(slug="burger-addons").first()
        if addon_category is None:
            missing.append("category: burger-addons")
        else:
            next_sort = (
                MenuItem.objects.filter(category=addon_category)
                .order_by("-sort_order")
                .values_list("sort_order", flat=True)
                .first()
                or 0
            )

            for offset, data in enumerate(MISSING_BURGER_ADDONS, start=1):
                item = MenuItem.objects.filter(slug=data["slug"]).first()
                if item is None:
                    self.stdout.write(
                        f"CREATE {addon_category.name} | {data['english_name']}: {data['price']:,}"
                    )
                    if not dry_run:
                        MenuItem.objects.create(
                            category=addon_category,
                            name=data["name"],
                            english_name=data["english_name"],
                            slug=data["slug"],
                            price=data["price"],
                            is_available=True,
                            sort_order=next_sort + offset,
                        )
                    created += 1

        for category_slug, fixes in verified_price_groups():
            category = Category.objects.filter(slug=category_slug).first()
            if not category:
                if f"category: {category_slug}" not in missing:
                    missing.append(f"category: {category_slug}")
                continue

            items = list(MenuItem.objects.filter(category=category))

            # Include would-be missing add-ons during dry-run so they do not show as false unmatched.
            virtual_addons = {}
            if dry_run and category_slug == "burger-addons":
                for data in MISSING_BURGER_ADDONS:
                    virtual_addons[normalize(data["english_name"])] = data

            index = {}
            for item in items:
                for candidate in (item.english_name, item.name):
                    key = normalize(candidate)
                    if key:
                        index.setdefault(key, []).append(item)

            for aliases, target_price in fixes:
                item = None
                for alias in aliases:
                    matches = index.get(normalize(alias), [])
                    if len(matches) == 1:
                        item = matches[0]
                        break

                if item is None:
                    if dry_run and category_slug == "burger-addons":
                        virtual = None
                        for alias in aliases:
                            virtual = virtual_addons.get(normalize(alias))
                            if virtual:
                                break
                        if virtual:
                            continue
                    missing.append(f"{category_slug}: {aliases[0]}")
                    continue

                if item.price == target_price:
                    correct += 1
                    continue

                self.stdout.write(
                    f"{category.name} | {item.english_name or item.name}: "
                    f"{item.price:,} -> {target_price:,}"
                )
                if not dry_run:
                    item.price = target_price
                    item.save(update_fields=["price"])
                changed += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Created missing items: {created}"))
        self.stdout.write(self.style.SUCCESS(f"Changed prices: {changed}"))
        self.stdout.write(f"Already correct: {correct}")
        if missing:
            self.stdout.write(self.style.WARNING("Unmatched entries:"))
            for value in missing:
                self.stdout.write(f"  - {value}")
        else:
            self.stdout.write(self.style.SUCCESS("Unmatched entries: 0"))
        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run only; database was not changed."))
