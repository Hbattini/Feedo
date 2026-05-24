from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Ingest Open Pet Food Facts cat food records through the deterministic pipeline."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=500)

    def handle(self, *args, **options):
        raise NotImplementedError("OPFF ingestion command scaffolded; implementation deferred.")
