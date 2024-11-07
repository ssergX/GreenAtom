from django.test import TestCase
from ..models import Storage, Organization


class StorageModelTest(TestCase):
    def setUp(self):
        self.storage = Storage.objects.create(
            name="Test Storage",
            latitude=55.7558,
            longitude=37.6176,
        )

    def test_storage_creation(self):
        self.assertEqual(self.storage.name, "Test Storage")
        self.assertEqual(self.storage.latitude, 55.7558)
        self.assertEqual(self.storage.longitude, 37.6176)

    def test_default_max_waste(self):
        self.assertEqual(self.storage.max_capacity, {"стекло": 1000, "биоотходы": 1000, "пластик": 1000})


class OrganizationModelTest(TestCase):
    def setUp(self):
        self.storage = Storage.objects.create(
            name="Test Storage",
            latitude=55.7558,
            longitude=37.6176,
        )

        self.organization = Organization.objects.create(
            name="Test Organization",
            latitude=55.7559,
            longitude=37.6177,
            waste_generated={"стекло": 200},
        )

    def test_automatic_linking_nearest_storage(self):
        self.assertEqual(self.organization.storage.name, "Test Storage")

    def test_organization_creation(self):
        self.assertEqual(self.organization.name, "Test Organization")
        self.assertEqual(self.organization.latitude, 55.7559)
        self.assertEqual(self.organization.longitude, 37.6177)

    def test_update_current_waste(self):
        self.storage.update_current_waste()
        self.assertEqual(self.storage.current_waste, self.organization.waste_generated)

    def test_find_closest_storage(self):
        # Проверка метода find_closest_storage, если у нас есть несколько хранилищ
        other_storage = Storage.objects.create(
            name="Another Storage",
            latitude=55.7560,
            longitude=37.6180,
            current_waste={"стекло": 200},
            max_capacity={"стекло": 1000, "биоотходы": 1000, "пластик": 1000}
        )

        # Применяем метод поиска ближайшего хранилища
        closest_storage = self.organization.find_closest_storage([self.storage, other_storage])

        # Проверяем, что метод выбрал правильное хранилище (по минимальному расстоянию)
        self.assertEqual(closest_storage.name, "Test Storage")
