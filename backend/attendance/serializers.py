from rest_framework import serializers
from .models import Attendance
from employees.models import Employee
from mongoengine.errors import DoesNotExist
from datetime import datetime

class EmployeeSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    employee_id = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    department = serializers.CharField(read_only=True)

    def to_representation(self, instance):
        return {
            'id': str(instance.id),
            'employee_id': instance.employee_id,
            'full_name': instance.full_name,
            'email': instance.email,
            'department': instance.department
        }

class AttendanceSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    employee = serializers.CharField(read_only=True)
    employee_details = EmployeeSerializer(read_only=True)
    employee_id = serializers.CharField(write_only=True)
    date = serializers.DateField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_employee_id(self, value):
        try:
            employee = Employee.objects.get(employee_id=value)
            return employee
        except DoesNotExist:
            raise serializers.ValidationError("Employee not found")

    def validate_status(self, value):
        if value not in ['Present', 'Absent']:
            raise serializers.ValidationError("Status must be either 'Present' or 'Absent'")
        return value

    def validate(self, attrs):
        employee = attrs.get('employee_id')
        date = attrs.get('date')
        
        # Check for duplicate attendance
        existing = Attendance.objects(employee=employee, date=date).first()
        if existing:
            raise serializers.ValidationError("Attendance already marked for this employee on this date")
        
        return attrs

    def create(self, validated_data):
        employee = validated_data.pop('employee_id')
        validated_data['employee'] = employee
        attendance = Attendance(**validated_data)
        attendance.save()
        return attendance

    def to_representation(self, instance):
        return {
            'id': str(instance.id),
            'employee': str(instance.employee.id),
            'employee_details': EmployeeSerializer(instance.employee).data,
            'date': instance.date,
            'status': instance.status,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }