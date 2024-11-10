from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CrudSerializer(serializers.ModelSerializer):
    """
    Base serializer class for CRUD.
    """

    class Meta:
        model = None  # This should be defined in the child class
        fields = None  # This should be defined in the child class

    def __init__(self, *args, **kwargs):
        # Ensure that the 'model' and 'fields' are set in the child class Meta
        if not self.Meta.model:
            raise ImproperlyConfigured("Django Access Point: The 'model' attribute must be defined in the child class Meta.")
        if not self.Meta.fields:
            raise ImproperlyConfigured("Django Access Point: The 'fields' attribute must be defined in the child class Meta.")

        # Get the custom field model from the context
        self.custom_field_model = self.context.get('custom_field_model', None)
        if not self.custom_field_model:
            raise ImproperlyConfigured("Django Access Point: The 'custom_field_model' must be provided in the context.")

        super().__init__(*args, **kwargs)

    def validate(self, data):
        """
        Custom validation to handle custom fields dynamically.
        """
        custom_fields_data = {}

        # Extract custom fields from the form data
        for key, value in self.initial_data.items():
            if key.startswith("custom_field_"):
                custom_field_id = key.split("_")[2]  # Extract the field ID (e.g., id1, id2)
                try:
                    custom_field = self.custom_field_model.objects.get(id=custom_field_id)
                except self.custom_field_model.DoesNotExist:
                    raise ValidationError(f"Custom field with ID {custom_field_id} does not exist.")
                custom_fields_data[custom_field_id] = value  # Store custom field value by its ID

        # Add custom fields data to the validated data
        data["custom_fields"] = custom_fields_data

        return data

    def create(self, validated_data):
        custom_fields_data = validated_data.pop("custom_fields", {})

        # Create the user object or other model as per the logic
        user = self.Meta.model.objects.create(**validated_data)

        # Save custom fields
        for field_id, value in custom_fields_data.items():
            try:
                custom_field = self.custom_field_model.objects.get(id=field_id)
                # Logic to save or associate the custom field with the user (e.g., create a relation)
                pass
            except self.custom_field_model.DoesNotExist:
                raise ValidationError(f"Custom field with ID {field_id} does not exist.")

        return user
