from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mongoengine.errors import NotUniqueError, DoesNotExist
from .models import Employee
from .serializers import EmployeeSerializer

@api_view(['GET', 'POST'])
def employee_list(request):
    if request.method == 'GET':
        employees = Employee.objects.all().order_by('-created_at')
        serializer = EmployeeSerializer(employees, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'count': len(serializer.data)
        })

    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                employee = serializer.save()
                return Response({
                    'success': True,
                    'message': 'Employee created successfully',
                    'data': EmployeeSerializer(employee).data
                }, status=status.HTTP_201_CREATED)
            except NotUniqueError:
                return Response({
                    'success': False,
                    'message': 'Employee ID already exists'
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'success': False,
            'message': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'DELETE'])
# def employee_detail(request, pk):
#     try:
#         employee = Employee.objects.get(id=pk)
#     except DoesNotExist:
#         return Response({
#             'success': False,
#             'message': 'Employee not found'
#         }, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = EmployeeSerializer(employee)
#         return Response({
#             'success': True,
#             'data': serializer.data
#         })

#     elif request.method == 'DELETE':
#         employee.delete()
#         return Response({
#             'success': True,
#             'message': 'Employee deleted successfully'
#         }, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'DELETE'])
def employee_detail(request, pk):
    # 1️⃣ Validate ObjectId
    # if not ObjectId.is_valid(pk):
    #     return Response(
    #         {
    #             'success': False,
    #             'message': 'Invalid employee ID'
    #         },
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

    try:
        # 2️⃣ Fetch using MongoEngine
        employee = Employee.objects.get(id=pk)

    except DoesNotExist:
        return Response(
            {
                'success': False,
                'message': 'Employee not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # ---------------- GET ----------------
    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    # ---------------- DELETE ----------------
    elif request.method == 'DELETE':
        employee.delete()
        return Response(
            {
                'success': True,
                'message': 'Employee deleted successfully'
            },
            status=status.HTTP_200_OK
        )
