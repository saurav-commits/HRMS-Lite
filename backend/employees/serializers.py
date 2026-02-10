from rest_framework import serializers
from .models import Employee
from mongoengine.errors import NotUniqueError

class EmployeeSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    employee_id = serializers.CharField(max_length=20)
    full_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    department = serializers.CharField(max_length=50)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_employee_id(self, value):
        if not value.strip():
            raise serializers.ValidationError("Employee ID is required")
        return value.strip()

    def validate_full_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Full name is required")
        return value.strip()

    def validate_email(self, value):
        if not value.strip():
            raise serializers.ValidationError("Email is required")
        return value.strip().lower()

    def validate_department(self, value):
        if not value.strip():
            raise serializers.ValidationError("Department is required")
        return value.strip()

    def create(self, validated_data):
        try:
            employee = Employee(**validated_data)
            employee.save()
            return employee
        except NotUniqueError:
            raise serializers.ValidationError("Employee ID already exists")

    def to_representation(self, instance):
        return {
            'id': str(instance.id),
            'employee_id': instance.employee_id,
            'full_name': instance.full_name,
            'email': instance.email,
            'department': instance.department,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }