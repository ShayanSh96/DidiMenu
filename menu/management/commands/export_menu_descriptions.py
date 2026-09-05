import json
from django.core.management.base import BaseCommand
from menu.models import MenuItem


class Command(BaseCommand):
    help = "Export menu descriptions for bilingual translation review."

    def handle(self, *args, **options):
        rows = []
        for item in MenuItem.objects.select_related("category").order_by(
            "category__sort_order", "sort_order", "name"
        ):
            if item.description:
                rows.append({
                    "slug": item.slug,
                    "name": item.name,
                    "english_name": item.english_name,
                    "description_fa": item.description,
                    "description_en": item.description_en,
                })

        output = json.dumps(rows, ensure_ascii=False, indent=2)
        with open("menu_descriptions.json", "w", encoding="utf-8") as f:
            f.write(output)

        self.stdout.write(self.style.SUCCESS(
            f"Exported {len(rows)} descriptions to menu_descriptions.json"
        ))
