from django.core.management.base import BaseCommand
from ...models import Storage, Organization


class Command(BaseCommand):
    help = 'Creates test data in the database'

    def handle(self, *args, **kwargs):
        storage1 = Storage.objects.create(
            name="Main Storage",
            latitude=55.7558,
            longitude=37.6176,
        )

        storage2 = Storage.objects.create(
            name="Secondary Storage",
            latitude=55.7512,
            longitude=37.6183,
        )

        organization1 = Organization.objects.create(
            name="Eco Solutions",
            latitude=55.760,
            longitude=37.620,
            waste_generated={"стекло": 50, "биоотходы": 30},
            storage=storage1
        )

        organization2 = Organization.objects.create(
            name="Green Corp",
            latitude=55.770,
            longitude=37.630,
            waste_generated={"пластик": 20, "биоотходы": 25},
            storage=storage2
        )

        self.stdout.write(self.style.SUCCESS('Test data created successfully'))
