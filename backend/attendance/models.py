from mongoengine import Document, ReferenceField, DateField, StringField, DateTimeField
from employees.models import Employee
from datetime import datetime

class Attendance(Document):
    ATTENDANCE_CHOICES = ['Present', 'Absent']
    
    employee = ReferenceField(Employee, required=True)
    date = DateField(required=True)
    status = StringField(max_length=10, choices=ATTENDANCE_CHOICES, required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'attendance',
        'indexes': [
            ('employee', 'date'),  # Compound index for uniqueness
            'date',
            'status'
        ]
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} - {self.status}"