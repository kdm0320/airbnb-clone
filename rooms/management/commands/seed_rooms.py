from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms import models as room_models
from users.models import models as user_models


class Command(BaseCommand):

    help = "This command creates rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many rooms you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(room_models.Room, number)
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))
