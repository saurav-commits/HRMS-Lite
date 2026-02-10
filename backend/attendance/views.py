from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mongoengine.errors import DoesNotExist
from .models import Attendance
from .serializers import AttendanceSerializer
from employees.models import Employee
from datetime import datetime

@api_view(['GET', 'POST'])
def attendance_list(request):
    if request.method == 'GET':
        employee_id = request.GET.get('employee_id')
        date = request.GET.get('date')
        
        queryset = Attendance.objects.all()
        print("qrrrr",queryset)
        
        if employee_id:
            try:
                employee = Employee.objects.get(employee_id=employee_id)
                queryset = queryset.filter(employee=employee)
            except DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Employee not found'
                }, status=status.HTTP_404_NOT_FOUND)
        
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(date=date_obj)
            except ValueError:
                return Response({
                    'success': False,
                    'message': 'Invalid date format. Use YYYY-MM-DD'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        attendance_records = queryset.order_by('-date', '-created_at')
        print("attendance records", attendance_records)
        serializer = AttendanceSerializer(attendance_records, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'count': len(serializer.data)
        })

    elif request.method == 'POST':
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                attendance = serializer.save()
                return Response({
                    'success': True,
                    'message': 'Attendance marked successfully',
                    'data': AttendanceSerializer(attendance).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'success': False,
                    'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'success': False,
            'message': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def employee_attendance_summary(request, employee_id):
    try:
        employee = Employee.objects.get(employee_id=employee_id)
    except DoesNotExist:
        return Response({
            'success': False,
            'message': 'Employee not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    attendance_records = Attendance.objects.filter(employee=employee)
    total_days = attendance_records.count()
    present_days = attendance_records.filter(status='Present').count()
    absent_days = attendance_records.filter(status='Absent').count()
    
    return Response({
        'success': True,
        'data': {
            'employee': {
                'id': str(employee.id),
                'employee_id': employee.employee_id,
                'full_name': employee.full_name,
                'department': employee.department
            },
            'summary': {
                'total_days': total_days,
                'present_days': present_days,
                'absent_days': absent_days,
                'attendance_percentage': round((present_days / total_days * 100), 2) if total_days > 0 else 0
            }
        }
    })