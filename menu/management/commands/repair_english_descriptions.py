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
        "sl": "fa",
        "tl": "en",
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
    help = "Repair English descriptions from Persian descriptions. Only description_en is modified."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite non-empty English descriptions too.",
        )

    def handle(self, *args, **options):
        force = options["force"]
        items = list(MenuItem.objects.all().order_by("id"))
        updated = 0
        skipped = 0
        failed = []

        self.stdout.write(f"English repair: {len(items)} menu item(s) found.")

        for index, item in enumerate(items, start=1):
            current = (item.description_en or "").strip()
            source = (item.description or "").strip()

            if not source:
                skipped += 1
                self.stdout.write(f"[{index}/{len(items)}] SKIP {item.slug} (no Persian description)")
                continue

            if current and not force:
                skipped += 1
                self.stdout.write(f"[{index}/{len(items)}] SKIP {item.slug} (English already exists)")
                continue

            try:
                translated = translate_text(source)
                if not translated:
                    raise CommandError("Translator returned an empty result")

                with transaction.atomic():
                    MenuItem.objects.filter(pk=item.pk).update(
                        description_en=translated,
                    )

                updated += 1
                self.stdout.write(self.style.SUCCESS(
                    f"[{index}/{len(items)}] UPDATED {item.slug}"
                ))
                time.sleep(0.15)
            except Exception as exc:
                failed.append((item.slug, str(exc)))
                self.stderr.write(self.style.ERROR(
                    f"[{index}/{len(items)}] FAILED {item.slug}: {exc}"
                ))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Updated: {updated}"))
        self.stdout.write(f"Skipped: {skipped}")
        self.stdout.write(f"Failed: {len(failed)}")

        if failed:
            self.stdout.write(self.style.WARNING(
                "Run the same command again. Completed rows stay untouched unless --force is used."
            ))
