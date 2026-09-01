import re
import unicodedata

from django.core.management.base import BaseCommand

from menu.models import Category, MenuItem


# Prices are in toman. Source menu values such as 108T mean 108,000 toman.
PRICE_GROUPS = [
    ("breakfast", [
        (("New Mexico",), 420_000), (("Sunny Turkey",), 590_000),
        (("Sweet & Savory", "Sweet and Savory"), 630_000), (("Avo Supreme",), 740_000),
        (("Hash Brown",), 590_000), (("Hot Pot Haricot",), 420_000),
        (("Egg Brisket",), 1_260_000), (("Heaven Plate",), 740_000),
    ]),
    ("iranian-breakfast", [
        (("Fried Egg",), 390_000), (("Omelet",), 390_000),
        (("Sausage Omelet",), 490_000), (("Sausage Omelette",), 490_000),
        (("Egg Fried with Ghormeh", "Egg Fried With Ghormeh"), 1_260_000),
    ]),
    ("hot-coffee", [
        (("Cinnamon Latte",), 250_000), (("Espresso",), 220_000),
        (("Americano", "Amerikano"), 220_000), (("Cortado", "Coctado"), 260_000),
        (("Cappuccino",), 210_000), (("Latte",), 220_000),
        (("Popcorn Latte",), 240_000), (("Mocha",), 250_000), (("Cream Mocha",), 270_000),
    ]),
    ("cold-coffee", [
        (("Cinnamon Ice Latte",), 250_000), (("Tonic Espresso",), 220_000),
        (("DIDI Wine Brew", "DiDi Wine Brew"), 250_000), (("Affogato",), 270_000),
        (("Irish Ice Latte",), 240_000), (("Caramel Ice Latte",), 240_000),
        (("Ice Mocha",), 250_000), (("Coco Ice Latte",), 250_000),
        (("Ice Latte",), 220_000), (("Ice Americano",), 220_000),
    ]),
    ("hot-drinks", [
        (("Ice Chocolate",), 200_000), (("Masala Tea", "Masah Tea"), 250_000),
        (("Karak Tea",), 250_000), (("Mint Chocolate",), 210_000), (("Hot Chocolate",), 200_000),
    ]),
    ("tea-herbal", [
        (("Black Tea",), 160_000), (("Saffron Tea",), 190_000),
        (("Eternal Herbal Tea",), 220_000), (("Charming Herbal Tea",), 220_000),
        (("Asheghaneh Herbal Tea",), 220_000), (("Shokraneh Herbal Tea",), 220_000),
        (("Shahaneh Herbal Tea",), 240_000), (("Jananeh Herbal Tea",), 220_000),
    ]),
    ("mocktails", [
        (("Pina Colada",), 250_000), (("Bloody",), 240_000), (("Martini",), 250_000),
        (("Miami Sunrise",), 240_000), (("New York City",), 220_000), (("Big Bang",), 250_000),
        (("Lovers",), 280_000), (("Khiar Sekanjebin", "Khiar Sekanjabin"), 240_000),
    ]),
    ("bakery", [
        (("Chocolate Twist",), 210_000), (("Swiss Bun with Chocolate",), 210_000),
        (("Chocolate Walnut Cookie",), 180_000), (("Double Chocolate Cookie",), 180_000),
        (("Oatmeal and Cranberry Diet Cookie", "Oatmeal & Cranberry Diet Cookie"), 180_000),
        (("Butter Croissant",), 220_000),
    ]),
    ("desserts", [
        (("Pina Colada Tart",), 220_000), (("Snickers Cake",), 280_000),
        (("Chocolate & Raspberry Tart", "Chocolate and Raspberry Tart"), 220_000),
        (("Mango Mousse",), 210_000), (("Banoffee",), 220_000),
        (("Three Milk Pistachio Cake",), 420_000), (("San Sebastian",), 280_000),
        (("Caramel & Filbert Tart", "Caramel and Filbert Tart"), 300_000), (("Pistachio Tart",), 440_000),
    ]),
    ("natural-drinks", [
        (("Ice Cream Carrot",), 250_000), (("Pomo Berry",), 220_000),
        (("Sparkle",), 220_000), (("Orange Peach",), 250_000),
    ]),
    ("smoothies", [
        (("Faloode Bastani",), 420_000), (("Tropical Style",), 220_000),
        (("Berry Style",), 220_000), (("Margarita Style",), 280_000),
    ]),
    ("milkshakes", [
        (("Chocolate Milkshake",), 440_000), (("Coconut Milkshake",), 420_000),
        (("Cookie Milkshake",), 450_000), (("Popcorn Milkshake",), 290_000),
    ]),
    ("fizzy-bar", [
        (("Texas Soda",), 118_000), (("Soda", "Soda Lemon", "Lemon Soda"), 108_000),
        (("Rogers Cola",), 128_000), (("Apple Soda",), 118_000),
        (("Classic Beer",), 170_000), (("Airish Beer", "Irish Beer"), 200_000),
        (("Coca Ice Cream",), 180_000), (("Grape Beer",), 220_000),
        (("Lemonade",), 190_000), (("Mojito",), 175_000), (("American Mojito",), 225_000),
    ]),
    ("bar-addons", [
        (("Saffron Syrup",), 60_000), (("Chocolate Syrup",), 60_000), (("Coconut Syrup",), 60_000),
        (("Hazelnut Syrup", "Hezelnut Syrup"), 60_000), (("Vanilla Syrup",), 60_000),
        (("Creamy Side",), 70_000), (("Shot of Milk", "Shot Of Milk"), 60_000),
    ]),
    ("brewed-coffee", [
        (("Turkish Coffee",), 180_000), (("Chemex",), 420_000), (("V60",), 420_000),
        (("Cold Brew",), 220_000), (("Clever",), 420_000), (("Regular Coffee",), 180_000),
    ]),
    ("appetizers", [
        (("Cucumber Yogurt", "Cacumber Yogurt"), 650_000), (("Caesar Salad",), 750_000),
        (("Avocado Salad",), 850_000), (("Season Salad",), 400_000), (("Fries",), 480_000),
        (("Chicken Wings Plate",), 540_000), (("Classic Hummus",), 410_000),
    ]),
    ("pizza-xl", [
        (("Chicken Pesto Pizza",), 1_220_000), (("Garlic & Steak Pizza", "Garlic and Steak Pizza"), 1_460_000),
        (("Pepperoni Pizza",), 1_120_000), (("Chicken Spinach Pizza",), 1_160_000),
        (("Bacon Spinach Pizza",), 1_280_000), (("Margherita Pizza",), 790_000),
        (("Parmigiano Pizza",), 1_480_000),
    ]),
    ("pizza-large", [
        (("Chicken Pesto Pizza",), 720_000), (("Pulled Beef Pizza", "Pold Beef Pizza"), 860_000),
        (("Garlic & Steak Pizza", "Garlic and Steak Pizza"), 840_000), (("Pepperoni Pizza",), 690_000),
        (("Chicken Spinach Pizza",), 640_000), (("Bacon Spinach Pizza",), 720_000),
        (("Margherita Pizza",), 590_000), (("Bacon Cream Pizza",), 880_000),
    ]),
    ("pasta", [(("Chicken Alfredo Pasta",), 760_000)]),
    ("steak", [
        (("Blaze & Butter Steaks", "Blaze and Butter Steaks"), 1_980_000),
        (("Scottish Steak",), 2_200_000), (("Dakota Chicken",), 960_000),
    ]),
    ("king-burger", [
        (("Rib Burger",), 1_420_000), (("Chicken Burger",), 740_000),
        (("Spicy Chicken Burger",), 760_000), (("American King Burger",), 1_100_000),
        (("Bone Marrow Burger",), 1_490_000), (("Sausage Burger",), 1_290_000),
        (("Caramelized Burger",), 1_210_000), (("Spicy Camembert Burger",), 1_290_000),
        (("Mushroom Burger",), 1_100_000), (("Halloumi Mushroom Burger",), 1_290_000),
        (("Mexicano Burger",), 1_270_000),
    ]),
    ("burger-180", [
        (("Sausage Burger",), 1_050_000), (("Spicy Camembert Burger",), 1_050_000),
        (("Mushroom Halloumi Burger",), 1_050_000), (("Bone Marrow Burger",), 1_250_000),
        (("Caramelized Burger",), 950_000), (("Mushroom Burger",), 950_000),
        (("American King Burger",), 850_000), (("Mexicano Burger",), 1_070_000),
    ]),
    ("burger-addons", [
        (("Pepperoni",), 190_000), (("Pulled Beef",), 260_000), (("Grilled Chicken Breast",), 120_000),
        (("Gouda Slice",), 80_000), (("Halloumi Cheese",), 120_000), (("Jalapeno",), 20_000),
        (("Camembert Cheese",), 180_000), (("Fried Egg",), 60_000), (("Bacon",), 200_000),
        (("Sausage",), 180_000), (("Bone Marrow",), 460_000), (("Caramelized Onion",), 40_000),
        (("Red Onion",), 20_000),
    ]),
    ("plates", [
        (("Buffalo Plate",), 1_280_000), (("Brisket",), 1_620_000),
        (("Cuban Brisket",), 1_650_000), (("Cuban Chicken",), 880_000),
        (("Cuban Pulled Beef",), 980_000), (("Cowboy",), 2_960_000),
    ]),
]


def normalize(value):
    value = unicodedata.normalize("NFKC", value or "").casefold()
    return "".join(ch for ch in value if ch.isalnum())


class Command(BaseCommand):
    help = "Safely correct DIDI menu prices without changing images, descriptions, or availability."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        changed = 0
        correct = 0
        missing = []

        for category_slug, fixes in PRICE_GROUPS:
            category = Category.objects.filter(slug=category_slug).first()
            if not category:
                missing.append(f"category: {category_slug}")
                continue

            items = list(MenuItem.objects.filter(category=category))
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
        self.stdout.write(self.style.SUCCESS(f"Changed: {changed}"))
        self.stdout.write(f"Already correct: {correct}")
        if missing:
            self.stdout.write(self.style.WARNING("Unmatched entries:"))
            for value in missing:
                self.stdout.write(f"  - {value}")
        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run only; database was not changed."))
