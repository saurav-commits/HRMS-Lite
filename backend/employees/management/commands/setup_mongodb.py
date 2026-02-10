from django.core.management.base import BaseCommand
from django.conf import settings
import mongoengine
from employees.models import Employee
from attendance.models import Attendance
from datetime import datetime, date, timedelta
import random

class Command(BaseCommand):
    help = 'Setup MongoDB database with collections and optional sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sample-data',
            action='store_true',
            help='Create sample employees and attendance data',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Setting up MongoDB database for HRMS Lite...')
        )

        try:
            # Test MongoDB connection
            mongoengine.connection.get_connection()
            self.stdout.write(
                self.style.SUCCESS('✅ Connected to MongoDB successfully')
            )

            # Create indexes for Employee model
            Employee.ensure_indexes()
            self.stdout.write(
                self.style.SUCCESS('✅ Created indexes for Employee collection')
            )

            # Create indexes for Attendance model  
            Attendance.ensure_indexes()
            self.stdout.write(
                self.style.SUCCESS('✅ Created indexes for Attendance collection')
            )

            # Create sample data if requested
            if options['sample_data']:
                self.create_sample_data()

            self.stdout.write(
                self.style.SUCCESS('\n🎉 MongoDB database setup completed successfully!')
            )
            self.stdout.write(
                self.style.SUCCESS('You can now run: python manage.py runserver')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error setting up database: {e}')
            )
            self.stdout.write(
                self.style.ERROR('Please ensure MongoDB is running and accessible')
            )

    def create_sample_data(self):
        """Create sample employees and attendance data"""
        try:
            # Clear existing data
            Employee.objects.all().delete()
            Attendance.objects.all().delete()
            
            # Sample employees
            employees_data = [
                {
                    "employee_id": "EMP001",
                    "full_name": "John Doe", 
                    "email": "john.doe@company.com",
                    "department": "Engineering"
                },
                {
                    "employee_id": "EMP002",
                    "full_name": "Jane Smith",
                    "email": "jane.smith@company.com", 
                    "department": "HR"
                },
                {
                    "employee_id": "EMP003",
                    "full_name": "Mike Johnson",
                    "email": "mike.johnson@company.com",
                    "department": "Marketing"
                },
                {
                    "employee_id": "EMP004",
                    "full_name": "Sarah Wilson",
                    "email": "sarah.wilson@company.com",
                    "department": "Finance"
                }
            ]

            # Create employees
            employees = []
            for emp_data in employees_data:
                employee = Employee(**emp_data)
                employee.save()
                employees.append(employee)

            self.stdout.write(
                self.style.SUCCESS(f'✅ Created {len(employees)} sample employees')
            )

            # Create attendance data for the last 7 days
            today = date.today()
            attendance_count = 0

            for i in range(7):
                attendance_date = today - timedelta(days=i)
                
                for employee in employees:
                    # 85% chance of being present
                    status = "Present" if random.random() > 0.15 else "Absent"
                    
                    attendance = Attendance(
                        employee=employee,
                        date=attendance_date,
                        status=status
                    )
                    attendance.save()
                    attendance_count += 1

            self.stdout.write(
                self.style.SUCCESS(f'✅ Created {attendance_count} sample attendance records')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'⚠️ Error creating sample data: {e}')
            )