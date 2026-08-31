from django.core.management.base import BaseCommand
from django.db import transaction

from menu.models import Category, MenuItem


def t(value):
    return int(value) * 1000


CATEGORIES = [
    ("صبحانه", "breakfast"),
    ("صبحانه ایرانی", "iranian-breakfast"),
    ("قهوه‌های گرم", "hot-coffee"),
    ("قهوه‌های سرد", "cold-coffee"),
    ("نوشیدنی‌های گرم", "hot-drinks"),
    ("چای و دمنوش", "tea-herbal"),
    ("ماکتیل‌ها", "mocktails"),
    ("نان و شیرینی", "bakery"),
    ("دسر و شیرینی", "desserts"),
    ("آبمیوه‌های طبیعی", "natural-drinks"),
    ("اسموتی‌ها", "smoothies"),
    ("میلک‌شیک‌ها", "milkshakes"),
    ("فیزی بار", "fizzy-bar"),
    ("افزودنی بار", "bar-addons"),
    ("قهوه‌های دمی", "brewed-coffee"),
    ("پیش‌غذا", "appetizers"),
    ("پیتزا ایکس‌لارج", "pizza-xl"),
    ("پیتزا لارج", "pizza-large"),
    ("پاستا", "pasta"),
    ("استیک", "steak"),
    ("کینگ برگر", "king-burger"),
    ("برگر ۱۸۰ گرمی", "burger-180"),
    ("افزودنی برگر", "burger-addons"),
    ("پلیت", "plates"),
]

# category_slug, persian name, english name, slug, price (thousand toman), available
ITEMS = [
    ("breakfast", "نیو مکزیکو", "New Mexico", "new-mexico", 420, True),
    ("breakfast", "سانی ترکی", "Sunny Turkey", "sunny-turkey", 590, True),
    ("breakfast", "سوییت ساووری", "Sweet & Savory", "sweet-savory", 630, True),
    ("breakfast", "آوو سوپریم", "Avo Supreme", "avo-supreme", 740, True),
    ("breakfast", "هش براون", "Hash Brown", "hash-brown", 590, True),
    ("breakfast", "هات پات لوبیا", "Hot Pot Haricot", "hot-pot-haricot", 420, True),
    ("breakfast", "اگ بریسکت", "Egg Brisket", "egg-brisket", 1260, True),
    ("breakfast", "هون پلیت", "Heaven Plate", "heaven-plate", 740, True),
    ("iranian-breakfast", "نیمرو", "Fried Egg", "fried-egg", 390, True),
    ("iranian-breakfast", "املت", "Omelet", "omelet", 390, True),
    ("iranian-breakfast", "املت ساسیج", "Sausage Omelet", "sausage-omelet", 490, True),
    ("iranian-breakfast", "نیمرو ساسیج", "Sausage Omelette", "sausage-fried-egg", 490, True),
    ("iranian-breakfast", "نیمرو قرمه", "Egg Fried with Ghormeh", "egg-fried-ghormeh", 1260, True),
    ("hot-coffee", "لاته سینامون", "Cinnamon Latte", "cinnamon-latte", 250, True),
    ("hot-coffee", "اسپرسو", "Espresso", "espresso", 220, True),
    ("hot-coffee", "آمریکانو", "Americano", "americano", 220, True),
    ("hot-coffee", "کورتادو", "Cortado", "cortado", 260, True),
    ("hot-coffee", "کاپوچینو", "Cappuccino", "cappuccino", 210, True),
    ("hot-coffee", "لاته", "Latte", "latte", 220, True),
    ("hot-coffee", "لاته پاپکورن", "Popcorn Latte", "popcorn-latte", 240, True),
    ("hot-coffee", "موکا", "Mocha", "mocha", 250, True),
    ("hot-coffee", "موکا با خامه", "Cream Mocha", "cream-mocha", 270, True),
    ("cold-coffee", "آیس لاته سینامون", "Cinnamon Ice Latte", "cinnamon-ice-latte", 250, True),
    ("cold-coffee", "تونیک اسپرسو", "Tonic Espresso", "tonic-espresso", 220, True),
    ("cold-coffee", "دی‌دی واین برو", "DIDI Wine Brew", "didi-wine-brew", 250, True),
    ("cold-coffee", "آفوگاتو", "Affogato", "affogato", 270, True),
    ("cold-coffee", "آیس لاته آیریش", "Irish Ice Latte", "irish-ice-latte", 240, True),
    ("cold-coffee", "آیس لاته کارامل", "Caramel Ice Latte", "caramel-ice-latte", 240, True),
    ("cold-coffee", "آیس موکا", "Ice Mocha", "ice-mocha", 250, True),
    ("cold-coffee", "آیس لاته نارگیل", "Coco Ice Latte", "coco-ice-latte", 250, True),
    ("cold-coffee", "آیس لاته", "Ice Latte", "ice-latte", 220, True),
    ("cold-coffee", "آیس آمریکانو", "Ice Americano", "ice-americano", 220, True),
    ("hot-drinks", "آیس چاکلت", "Ice Chocolate", "ice-chocolate", 200, True),
    ("hot-drinks", "چای ماسالا", "Masala Tea", "masala-tea", 220, True),
    ("hot-drinks", "چای کرک", "Karak Tea", "karak-tea", 220, True),
    ("hot-drinks", "هات چاکلت نعنایی", "Mint Chocolate", "mint-chocolate", 210, True),
    ("hot-drinks", "هات چاکلت", "Hot Chocolate", "hot-chocolate", 200, True),
    ("tea-herbal", "چای سیاه", "Black Tea", "black-tea", 160, True),
    ("tea-herbal", "چای زعفران", "Saffron Tea", "saffron-tea", 190, True),
    ("tea-herbal", "دمنوش جاودانه", "Eternal Herbal Tea", "eternal-herbal-tea", 220, True),
    ("tea-herbal", "دمنوش دلبرانه", "Charming Herbal Tea", "charming-herbal-tea", 220, True),
    ("tea-herbal", "دمنوش عاشقانه", "Asheghaneh Herbal Tea", "asheghaneh-herbal-tea", 220, True),
    ("tea-herbal", "دمنوش شکرانه", "Shokraneh Herbal Tea", "shokraneh-herbal-tea", 220, True),
    ("tea-herbal", "دمنوش شاهانه", "Shahaneh Herbal Tea", "shahaneh-herbal-tea", 240, True),
    ("tea-herbal", "دمنوش جانانه", "Jananeh Herbal Tea", "jananeh-herbal-tea", 220, True),
    ("mocktails", "پیناکولادا", "Pina Colada", "pina-colada", 290, True),
    ("mocktails", "بلادی", "Bloody", "bloody", 240, True),
    ("mocktails", "مارتینی", "Martini", "martini", 290, True),
    ("mocktails", "میامی سانرایز", "Miami Sunrise", "miami-sunrise", 240, True),
    ("mocktails", "نیویورک سیتی", "New York City", "new-york-city", 220, True),
    ("mocktails", "بیگ بنگ", "Big Bang", "big-bang", 280, True),
    ("mocktails", "لاورز", "Lovers", "lovers", 290, True),
    ("mocktails", "خیار سکنجبین", "Khiar Sekanjebin", "khiar-sekanjebin", 240, True),
    ("bakery", "چاکلت توییست", "Chocolate Twist", "chocolate-twist", 210, True),
    ("bakery", "بن سوئیسی با سس شکلات", "Swiss Bun with Chocolate", "swiss-bun-chocolate", 210, True),
    ("bakery", "کوکی شکلات گردو", "Chocolate Walnut Cookie", "chocolate-walnut-cookie", 180, True),
    ("bakery", "کوکی دبل چاکلت", "Double Chocolate Cookie", "double-chocolate-cookie", 180, True),
    ("bakery", "کوکی رژیمی اوتمیل و کرن‌بری", "Oatmeal and Cranberry Diet Cookie", "oatmeal-cranberry-cookie", 180, True),
    ("bakery", "کروسان شکلاتی", "Chocolate Croissant", "chocolate-croissant", 0, False),
    ("bakery", "کروسان کره‌ای ساده", "Butter Croissant", "butter-croissant", 220, True),
    ("desserts", "تارت پیناکولادا", "Pina Colada Tart", "pina-colada-tart", 220, True),
    ("desserts", "کیک اسنیکرز", "Snickers Cake", "snickers-cake", 280, True),
    ("desserts", "تارت شکلات رزبری", "Chocolate & Raspberry Tart", "chocolate-raspberry-tart", 220, True),
    ("desserts", "موس انبه", "Mango Mousse", "mango-mousse", 210, True),
    ("desserts", "بانوفی", "Banoffee", "banoffee", 220, True),
    ("desserts", "کیک سه شیر پسته", "Three Milk Pistachio Cake", "three-milk-pistachio-cake", 420, True),
    ("desserts", "چیزکیک سن سباستین", "San Sebastian", "san-sebastian", 280, True),
    ("desserts", "تارت کارامل فندق", "Caramel & Filbert Tart", "caramel-filbert-tart", 300, True),
    ("desserts", "تارت پسته", "Pistachio Tart", "pistachio-tart", 440, True),
    ("natural-drinks", "آب هویج بستنی", "Ice Cream Carrot", "ice-cream-carrot", 250, True),
    ("natural-drinks", "پومو بری", "Pomo Berry", "pomo-berry", 220, True),
    ("natural-drinks", "اسپارکل", "Sparkle", "sparkle", 220, True),
    ("natural-drinks", "اورنج پیچ", "Orange Peach", "orange-peach", 250, True),
    ("smoothies", "فالوده بستنی مغزدار", "Faloode Bastani", "faloode-bastani", 420, True),
    ("smoothies", "امریکن استایل", "American Style", "american-style", 0, False),
    ("smoothies", "تروپیکال استایل", "Tropical Style", "tropical-style", 220, True),
    ("smoothies", "بری استایل", "Berry Style", "berry-style", 220, True),
    ("smoothies", "مارگاریتا استایل", "Margarita Style", "margarita-style", 280, True),
    ("milkshakes", "چاکلت شیک", "Chocolate Milkshake", "chocolate-milkshake", 440, True),
    ("milkshakes", "کوکو شیک", "Coconut Milkshake", "coconut-milkshake", 420, True),
    ("milkshakes", "کوکی شیک", "Cookie Milkshake", "cookie-milkshake", 450, True),
    ("milkshakes", "پاپ شیک", "Popcorn Milkshake", "popcorn-milkshake", 290, True),
    ("milkshakes", "پرو شیک", "Pro Milk Shake", "pro-milk-shake", 0, False),
    ("milkshakes", "ناتی شیک", "Nutty Milk Shake", "nutty-milk-shake", 0, False),
    ("fizzy-bar", "تگزاس سودا", "Texas Soda", "texas-soda", 110, True),
    ("fizzy-bar", "سودا لیمو", "Soda", "soda-lemon", 100, True),
    ("fizzy-bar", "راجرز کولا", "Rogers Cola", "rogers-cola", 120, True),
    ("fizzy-bar", "اپل سودا", "Apple Soda", "apple-soda", 110, True),
    ("fizzy-bar", "مالت کلاسیک", "Classic Beer", "classic-beer", 170, True),
    ("fizzy-bar", "مالت آیریش", "Airish Beer", "airish-beer", 200, True),
    ("fizzy-bar", "کوکا بستنی", "Coca Ice Cream", "coca-ice-cream", 180, True),
    ("fizzy-bar", "مالت انگور", "Grape Beer", "grape-beer", 220, True),
    ("fizzy-bar", "لیموناد کلاسیک", "Lemonade", "lemonade", 190, True),
    ("fizzy-bar", "موهیتو کلاسیک", "Mojito", "classic-mojito", 170, True),
    ("fizzy-bar", "امریکن موهیتو", "American Mojito", "american-mojito", 200, True),
    ("bar-addons", "سیروپ زعفران", "Saffron Syrup", "saffron-syrup", 60, True),
    ("bar-addons", "سیروپ شکلات", "Chocolate Syrup", "chocolate-syrup", 60, True),
    ("bar-addons", "سیروپ نارگیل", "Coconut Syrup", "coconut-syrup", 60, True),
    ("bar-addons", "سیروپ فندق", "Hazelnut Syrup", "hazelnut-syrup", 60, True),
    ("bar-addons", "سیروپ وانیل", "Vanilla Syrup", "vanilla-syrup", 60, True),
    ("bar-addons", "ساید خامه قنادی", "Creamy Side", "creamy-side", 70, True),
    ("bar-addons", "شات شیر", "Shot of Milk", "shot-of-milk", 60, True),
    ("brewed-coffee", "قهوه ترک", "Turkish Coffee", "turkish-coffee", 180, True),
    ("brewed-coffee", "کمکس", "Chemex", "chemex", 420, True),
    ("brewed-coffee", "وی ۶۰", "V60", "v60", 420, True),
    ("brewed-coffee", "کلد برو", "Cold Brew", "cold-brew", 220, True),
    ("brewed-coffee", "کلور", "Clever", "clever", 420, True),
    ("brewed-coffee", "رگولار امریکن استایل", "Regular Coffee", "regular-coffee", 180, True),
    ("appetizers", "آب دوغ خیار", "Cucumber Yogurt", "cucumber-yogurt", 650, True),
    ("appetizers", "سالاد سزار", "Caesar Salad", "caesar-salad", 750, True),
    ("appetizers", "سالاد آووکادو", "Avocado Salad", "avocado-salad", 850, True),
    ("appetizers", "سیزن سالاد", "Season Salad", "season-salad", 400, True),
    ("appetizers", "فرنچ فرایز", "Fries", "fries", 480, True),
    ("appetizers", "چیکن وینگز پلیت", "Chicken Wings Plate", "chicken-wings-plate", 540, True),
    ("appetizers", "حمص کلاسیک", "Classic Hummus", "classic-hummus", 410, True),
    ("pizza-xl", "پیتزا چیکن پستو", "Chicken Pesto Pizza", "xl-chicken-pesto-pizza", 1220, True),
    ("pizza-xl", "پیتزا اسپشیال", "Special Pizza", "xl-special-pizza", 0, False),
    ("pizza-xl", "پیتزا پولد بیف", "Pulled Beef Pizza", "xl-pulled-beef-pizza", 0, False),
    ("pizza-xl", "پیتزا بلونز", "Bolognese Pizza", "xl-bolognese-pizza", 0, False),
    ("pizza-xl", "پیتزا سیر و استیک", "Garlic & Steak Pizza", "xl-garlic-steak-pizza", 1460, True),
    ("pizza-xl", "پیتزا پپرونی", "Pepperoni Pizza", "xl-pepperoni-pizza", 1120, True),
    ("pizza-xl", "پیتزا چیکن اسفناج", "Chicken Spinach Pizza", "xl-chicken-spinach-pizza", 1160, True),
    ("pizza-xl", "پیتزا بیکن اسفناج", "Bacon Spinach Pizza", "xl-bacon-spinach-pizza", 1280, True),
    ("pizza-xl", "پیتزا مارگاریتا", "Margherita Pizza", "xl-margherita-pizza", 790, True),
    ("pizza-xl", "پیتزا کرم بیکن", "Parmigiano Pizza", "xl-parmigiano-pizza", 1480, True),
    ("pizza-large", "پیتزا چیکن پستو", "Chicken Pesto Pizza", "large-chicken-pesto-pizza", 720, True),
    ("pizza-large", "پیتزا اسپشیال", "Special Pizza", "large-special-pizza", 0, False),
    ("pizza-large", "پیتزا پولد بیف", "Pulled Beef Pizza", "large-pulled-beef-pizza", 860, True),
    ("pizza-large", "پیتزا بلونز", "Bolognese Pizza", "large-bolognese-pizza", 0, False),
    ("pizza-large", "پیتزا سیر و استیک", "Garlic and Steak Pizza", "large-garlic-steak-pizza", 840, True),
    ("pizza-large", "پیتزا پپرونی", "Pepperoni Pizza", "large-pepperoni-pizza", 690, True),
    ("pizza-large", "پیتزا چیکن اسفناج", "Chicken Spinach Pizza", "large-chicken-spinach-pizza", 640, True),
    ("pizza-large", "پیتزا بیکن اسفناج", "Bacon Spinach Pizza", "large-bacon-spinach-pizza", 720, True),
    ("pizza-large", "پیتزا مارگاریتا", "Margherita Pizza", "large-margherita-pizza", 590, True),
    ("pizza-large", "پیتزا کرم بیکن", "Bacon Cream Pizza", "large-bacon-cream-pizza", 880, True),
    ("pasta", "لازانیا بلونز", "Beef Lasagna", "beef-lasagna", 0, False),
    ("pasta", "لازانیا پولد بیف", "Pulled Beef Lasagna", "pulled-beef-lasagna", 0, False),
    ("pasta", "لازانیا چیکن اسفناج", "Chicken & Spinach Lasagna", "chicken-spinach-lasagna", 0, False),
    ("pasta", "پاستا چیکن آلفردو", "Chicken Alfredo Pasta", "chicken-alfredo-pasta", 760, True),
    ("steak", "استیک بلیز اند باتر", "Blaze & Butter Steaks", "blaze-butter-steaks", 1980, True),
    ("steak", "استیک انترکوت", "Entrecote Steak", "entrecote-steak", 0, False),
    ("steak", "استیک اوهایو", "Ohio Steak", "ohio-steak", 0, False),
    ("steak", "استیک اسکاتلندی", "Scottish Steak", "scottish-steak", 2200, True),
    ("steak", "استیک وگاس", "Vegas Steak", "vegas-steak", 0, False),
    ("steak", "دکوتا چیکن", "Dakota Chicken", "dakota-chicken", 990, True),
    ("king-burger", "ریپ برگر", "Rib Burger", "king-rib-burger", 1420, True),
    ("king-burger", "چیکن برگر کلاسیک", "Chicken Burger", "king-chicken-burger", 740, True),
    ("king-burger", "چیکن برگر اسپایسی", "Spicy Chicken Burger", "king-spicy-chicken-burger", 760, True),
    ("king-burger", "کینگ برگر آمریکایی", "American King Burger", "king-american-burger", 1180, True),
    ("king-burger", "بن مارو برگر", "Bone Marrow Burger", "king-bone-marrow-burger", 1400, True),
    ("king-burger", "ساسیج برگر", "Sausage Burger", "king-sausage-burger", 1250, True),
    ("king-burger", "کاراملایزد برگر", "Caramelized Burger", "king-caramelized-burger", 1210, True),
    ("king-burger", "بوفالو کممبر برگر", "Spicy Camembert Burger", "king-spicy-camembert-burger", 1250, True),
    ("king-burger", "ماشروم برگر", "Mushroom Burger", "king-mushroom-burger", 1180, True),
    ("king-burger", "هالومی ماشروم برگر", "Halloumi Mushroom Burger", "king-halloumi-mushroom-burger", 1250, True),
    ("king-burger", "مکزیکانو برگر", "Mexicano Burger", "king-mexicano-burger", 0, True),
    ("burger-180", "ساسیج برگر", "Sausage Burger", "180-sausage-burger", 1050, True),
    ("burger-180", "بوفالو کممبر برگر", "Spicy Camembert Burger", "180-spicy-camembert-burger", 1050, True),
    ("burger-180", "هالومی ماشروم برگر", "Mushroom Halloumi Burger", "180-halloumi-mushroom-burger", 1080, True),
    ("burger-180", "بن مارو برگر", "Bone Marrow Burger", "180-bone-marrow-burger", 1250, True),
    ("burger-180", "کاراملایزد برگر", "Caramelized Burger", "180-caramelized-burger", 980, True),
    ("burger-180", "ماشروم برگر", "Mushroom Burger", "180-mushroom-burger", 990, True),
    ("burger-180", "کینگ برگر آمریکایی", "American King Burger", "180-american-king-burger", 880, True),
    ("burger-180", "مکزیکانو برگر", "Mexicano Burger", "180-mexicano-burger", 1070, True),
    ("burger-addons", "پپرونی", "Pepperoni", "addon-pepperoni", 190, True),
    ("burger-addons", "پولد بیف", "Pulled Beef", "addon-pulled-beef", 390, True),
    ("burger-addons", "سینه مرغ گریل", "Grilled Chicken Breast", "addon-grilled-chicken", 120, True),
    ("burger-addons", "پنیر گودا ورقه‌ای", "Gouda Slice", "addon-gouda-slice", 90, True),
    ("burger-addons", "پنیر هالومی", "Halloumi Cheese", "addon-halloumi-cheese", 120, True),
    ("burger-addons", "هالوپینو", "Jalapeno", "addon-jalapeno", 30, True),
    ("burger-addons", "پنیر کممبر", "Camembert Cheese", "addon-camembert-cheese", 190, True),
    ("burger-addons", "نیمرو", "Fried Egg", "addon-fried-egg", 90, True),
    ("burger-addons", "بیکن", "Bacon", "addon-bacon", 200, True),
    ("burger-addons", "سس", "Sauce", "addon-sauce", 100, True),
    ("burger-addons", "بن مارو", "Bone Marrow", "addon-bone-marrow", 390, True),
    ("plates", "ساندویچ سوسیس", "Sausage Sandwich", "sausage-sandwich", 0, False),
    ("plates", "بشقاب سوسیس", "Sausage Plate", "sausage-plate", 0, False),
    ("plates", "بوفالو پلیت", "Buffalo Plate", "buffalo-plate", 1280, True),
    ("plates", "تاکو", "Taco", "taco", 0, False),
    ("plates", "بریسکت", "Brisket", "brisket", 1600, True),
    ("plates", "بریسکت کوبایی", "Cuban Brisket", "cuban-brisket", 1500, True),
    ("plates", "چیکن کوبایی", "Cuban Chicken", "cuban-chicken", 850, True),
    ("plates", "پولد بیف کوبایی", "Cuban Pulled Beef", "cuban-pulled-beef", 990, True),
    ("plates", "کابوی دیش", "Cowboy", "cowboy", 2960, True),
]


class Command(BaseCommand):
    help = "Seed DIDI menu categories and products from the current menu screenshots."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing categories and menu items before importing the DIDI menu.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            MenuItem.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing menu data removed."))

        categories = {}
        for index, (name, slug) in enumerate(CATEGORIES, start=1):
            category, _ = Category.objects.update_or_create(
                slug=slug,
                defaults={"name": name, "sort_order": index, "is_active": True},
            )
            categories[slug] = category

        created = 0
        updated = 0
        order_by_category = {}
        for category_slug, name, english_name, slug, price_thousands, available in ITEMS:
            order_by_category[category_slug] = order_by_category.get(category_slug, 0) + 1
            _, was_created = MenuItem.objects.update_or_create(
                slug=slug,
                defaults={
                    "category": categories[category_slug],
                    "name": name,
                    "english_name": english_name,
                    "description": "",
                    "price": t(price_thousands) if price_thousands else 0,
                    "is_available": available,
                    "is_featured": False,
                    "sort_order": order_by_category[category_slug],
                },
            )
            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(
            self.style.SUCCESS(
                f"DIDI menu imported: {len(CATEGORIES)} categories, "
                f"{created} products created, {updated} products updated."
            )
        )
