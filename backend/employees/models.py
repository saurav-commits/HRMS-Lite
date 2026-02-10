from mongoengine import Document, StringField, EmailField, DateTimeField
import re
from mongoengine.errors import ValidationError
from datetime import datetime

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError('Invalid email format')

class Employee(Document):
    employee_id = StringField(max_length=20, unique=True, required=True)
    full_name = StringField(max_length=100, required=True)
    email = EmailField(required=True, validation=validate_email)
    department = StringField(max_length=50, required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'employees',
        'indexes': ['employee_id', 'email']
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"