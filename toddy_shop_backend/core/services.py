from django.core.exceptions import ValidationError


class BaseService:
    """
    Base service class for domain logical operations.
    Any service methods that raise exceptions should catch them here or in custom exceptions.
    """

    pass


def validate_required_fields(data, required_fields):
    """
    Validates if the required fields are present in the provided data dictionary.
    """
    missing_fields = [
        field for field in required_fields if field not in data or not data.get(field)
    ]
    if missing_fields:
        raise ValidationError(
            {field: "This field is required." for field in missing_fields}
        )
