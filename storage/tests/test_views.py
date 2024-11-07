from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Storage
from ..serializers import StorageSerializer


class StorageAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.storage = Storage.objects.create(
            name="Test Storage",
            latitude=55.7558,
            longitude=37.6176,
            current_waste={"стекло": 100, "биоотходы": 50},
            max_capacity={"стекло": 1000, "биоотходы": 500, "пластик": 800},
        )

        self.url = f"/api/storages/{self.storage.id}/"

    def test_get_storage(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.storage.name)
        self.assertEqual(response.data['latitude'], self.storage.latitude)
        self.assertEqual(response.data['longitude'], self.storage.longitude)

    def test_create_storage(self):
        new_storage_data = {
            "name": "New Storage",
            "latitude": 55.7600,
            "longitude": 37.6200,
            "current_waste": {"стекло": 200, "биоотходы": 100},
            "max_capacity": {"стекло": 1000, "биоотходы": 500, "пластик": 800}
        }

        response = self.client.post("/api/storages/", new_storage_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], new_storage_data['name'])
        self.assertEqual(response.data['latitude'], new_storage_data['latitude'])
        self.assertEqual(response.data['longitude'], new_storage_data['longitude'])

    def test_update_storage(self):
        updated_data = {
            "name": "Updated Storage",
            "latitude": 55.7600,
            "longitude": 37.6200,
            "current_waste": {"стекло": 300, "биоотходы": 200},
            "max_capacity": {"стекло": 1000, "биоотходы": 500, "пластик": 800}
        }

        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])
        self.assertEqual(response.data['latitude'], updated_data['latitude'])
        self.assertEqual(response.data['longitude'], updated_data['longitude'])

    def test_partial_update_storage(self):
        partial_data = {
            "name": "Partially Updated Storage",
            "current_waste": {"стекло": 400}
        }

        response = self.client.patch(self.url, partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], partial_data['name'])
        self.assertEqual(response.data['current_waste'], partial_data['current_waste'])

    def test_delete_storage(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_create_storage(self):
        invalid_data = {
            "name": "",  # Пустое имя
            "latitude": 200.0,  # Некорректная широта
            "longitude": 200.0,  # Некорректная долгота
            "current_waste": {"стекло": 200},
            "max_capacity": {"стекло": 1000}
        }
        response = self.client.post("/api/storages/", invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_serializer_validation(self):
        storage_serializer = StorageSerializer(instance=self.storage)
        data = storage_serializer.data
        self.assertEqual(data['name'], self.storage.name)
        self.assertEqual(data['latitude'], self.storage.latitude)
        self.assertEqual(data['longitude'], self.storage.longitude)
