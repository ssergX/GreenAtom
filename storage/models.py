from django.db import models
from django.core.exceptions import ValidationError
from .validators import WasteValidator
from geopy.distance import great_circle


class Storage(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    current_waste = models.JSONField(validators=[WasteValidator.validate_waste_types], default=dict, blank=True)
    max_capacity = models.JSONField(validators=[WasteValidator.validate_capacity], default=dict, blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        # Задаем дефолтные значения для максимальной емкости, если они не указаны
        default_capacities = {
            "стекло": 1000,
            "биоотходы": 1000,
            "пластик": 1000
        }

        if not (-90 <= self.latitude <= 90):
            raise ValidationError(f"Широта '{self.latitude}' должна быть в диапазоне [-90, 90].")

        if not (-180.0 <= self.longitude <= 180.0):
            raise ValidationError(f"Долгота '{self.longitude}' должна быть в диапазоне [-180, 180].")

        if not isinstance(self.current_waste, dict):
            raise ValidationError("Текущий запас должен быть объектом (словарем).")

        if not isinstance(self.max_capacity, dict):
            raise ValidationError("Максимальная емкость должна быть объектом (словарем).")

        for waste_type, amount in self.current_waste.items():
            if amount > self.max_capacity.get(waste_type, 0):
                raise ValidationError(
                    f"Запас для '{waste_type}' не может превышать максимальную емкость {self.max_capacity.get(waste_type, 0)}."
                )

        for waste_type, default_amount in default_capacities.items():
            if waste_type not in self.max_capacity:
                self.max_capacity[waste_type] = default_amount

    @property
    def organizations_list(self):
        return self.organization_set.all()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def update_current_waste(self):

        current_waste = {}
        organizations = self.organization_set.all()

        for organization in organizations:
            for waste_type, amount in organization.waste_generated.items():
                current_waste[waste_type] = current_waste.get(waste_type, 0) + amount

        self.current_waste = current_waste
        self.save()


class Organization(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    waste_generated = models.JSONField(validators=[WasteValidator.validate_waste_types], default=dict, blank=True)
    storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, null=True, blank=True)  # Связь с хранилищем

    def __str__(self):
        return self.name

    def find_closest_storage(self, storages):
        suitable_storages = [
            storage for storage in storages if all(
                waste_type in storage.max_capacity and
                (storage.current_waste.get(waste_type, 0) + amount <= storage.max_capacity[waste_type])
                for waste_type, amount in self.waste_generated.items()
            )
        ]

        if not suitable_storages:
            return None

        closest_storage = min(
            suitable_storages,
            key=lambda storage: self.calculate_distance(storage)
        )
        return closest_storage

    def calculate_distance(self, storage):
        organization_location = (self.latitude, self.longitude)
        storage_location = (storage.latitude, storage.longitude)
        return great_circle(organization_location, storage_location).kilometers

    def save(self, *args, **kwargs):
        if not self.waste_generated:
            raise ValidationError("Не указаны отходы, которые генерирует организация.")

        storages = Storage.objects.all()
        closest_storage = self.find_closest_storage(storages)
        if closest_storage:
            self.storage = closest_storage
        else:
            raise ValidationError("Нет подходящих хранилищ для ваших отходов.")

        super().save(*args, **kwargs)
