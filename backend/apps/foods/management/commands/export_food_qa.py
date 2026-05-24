from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Export food records that need manual QA."

    def handle(self, *args, **options):
        raise NotImplementedError("Food QA export command scaffolded; implementation deferred.")
