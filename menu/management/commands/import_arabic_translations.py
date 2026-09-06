import json
import time
import urllib.parse
import urllib.request

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from menu.models import MenuItem


TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"


def translate_text(text):
    if not text:
        return ""

    params = urllib.parse.urlencode({
        "client": "gtx",
        "sl": "en",
        "tl": "ar",
        "dt": "t",
        "q": text,
    })
    request = urllib.request.Request(
        f"{TRANSLATE_URL}?{params}",
        headers={"User-Agent": "Mozilla/5.0"},
    )

    last_error = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return "".join(part[0] for part in payload[0] if part and part[0]).strip()
        except Exception as exc:
            last_error = exc
            time.sleep(2 * (attempt + 1))

    raise CommandError(f"Translation request failed: {last_error}")


class Command(BaseCommand):
    help = "Populate Arabic names and descriptions for all menu items without changing prices or Persian/English content."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Translate again even when Arabic fields already contain values.",
        )

    def handle(self, *args, **options):
        force = options["force"]
        items = list(MenuItem.objects.all().order_by("id"))
        updated = 0
        skipped = 0
        failed = []

        self.stdout.write(f"Arabic translation: {len(items)} menu item(s) found.")

        for index, item in enumerate(items, start=1):
            needs_name = force or not item.arabic_name.strip()
            needs_description = force or not item.description_ar.strip()

            if not needs_name and not needs_description:
                skipped += 1
                self.stdout.write(f"[{index}/{len(items)}] SKIP {item.slug}")
                continue

            try:
                source_name = (item.english_name or item.name).strip()
                source_description = (item.description_en or item.description).strip()

                arabic_name = item.arabic_name
                arabic_description = item.description_ar

                if needs_name:
                    arabic_name = translate_text(source_name)
                    time.sleep(0.15)

                if needs_description and source_description:
                    arabic_description = translate_text(source_description)
                    time.sleep(0.15)

                # Save only the two Arabic fields. Prices and all source content stay untouched.
                with transaction.atomic():
                    MenuItem.objects.filter(pk=item.pk).update(
                        arabic_name=arabic_name,
                        description_ar=arabic_description,
                    )

                updated += 1
                self.stdout.write(self.style.SUCCESS(
                    f"[{index}/{len(items)}] UPDATED {item.slug} -> {arabic_name}"
                ))
            except Exception as exc:
                failed.append((item.slug, str(exc)))
                self.stderr.write(self.style.ERROR(
                    f"[{index}/{len(items)}] FAILED {item.slug}: {exc}"
                ))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Updated: {updated}"))
        self.stdout.write(f"Already translated: {skipped}")
        self.stdout.write(f"Failed: {len(failed)}")

        if failed:
            self.stdout.write(self.style.WARNING(
                "Run the same command again; completed items will be skipped and only missing translations will retry."
            ))
