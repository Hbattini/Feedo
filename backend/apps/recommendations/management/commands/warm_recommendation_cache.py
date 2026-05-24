from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Warm recommendation cache for demo or local testing."

    def handle(self, *args, **options):
        raise NotImplementedError("Recommendation cache warming scaffolded; implementation deferred.")
