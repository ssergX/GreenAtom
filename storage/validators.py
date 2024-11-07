from django.core.exceptions import ValidationError


class WasteValidator:
    allowed_waste_types = ["биоотходы", "стекло", "пластик"]

    @staticmethod
    def validate_capacity(value):
        if not isinstance(value, dict):
            raise ValidationError("Максимальный запас должен быть объектом json.")

        for waste_type, amount in value.items():
            if waste_type not in WasteValidator.allowed_waste_types:
                raise ValidationError(f"Тип отхода '{waste_type}' не является допустимым.")
            if not isinstance(amount, int) or amount < 0:
                raise ValidationError(f"Запас для '{waste_type}' должен быть неотрицательным целым числом.")

    @staticmethod
    def validate_waste_types(value):
        if not isinstance(value, dict):
            raise ValidationError("Текущий запас должен быть объектом json.")

        for waste_type, amount in value.items():
            if waste_type not in WasteValidator.allowed_waste_types:
                raise ValidationError(f"Тип отхода '{waste_type}' не является допустимым.")
            if not isinstance(amount, int) or amount < 0:
                raise ValidationError(f"Запас для '{waste_type}' должен быть неотрицательным целым числом.")
