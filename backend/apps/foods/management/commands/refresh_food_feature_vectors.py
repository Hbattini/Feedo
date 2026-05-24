from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Regenerate feature_json from canonical food attributes."

    def handle(self, *args, **options):
        raise NotImplementedError("Feature vector refresh command scaffolded; implementation deferred.")
