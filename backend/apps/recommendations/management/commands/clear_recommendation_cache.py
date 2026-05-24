from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Clear recommendation cache entries for local debugging."

    def handle(self, *args, **options):
        raise NotImplementedError("Recommendation cache clearing scaffolded; implementation deferred.")
