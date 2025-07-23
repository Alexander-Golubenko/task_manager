from django.utils.timezone import now
from rest_framework import serializers


def validate_deadline(value):
    if value < now().date():
        raise serializers.ValidationError('Deadline cannot be before today')
    return value