from django.db.models.functions import ExtractWeekDay
from rest_framework.decorators import api_view
from rest_framework.response import  Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import  Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer, SubTaskCreateSerializer
from django.utils.timezone import now
from rest_framework.views import  APIView

@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskListView(APIView):
    def get(self, request):
        weekday_name = request.query_params.get('weekday')
        queryset = Task.objects.all()

        if weekday_name:
            weekday_name = weekday_name.capitalize()
            weekdays_dict = {
                'Monday': 2, 'Понедельник': 2,
                'Tuesday': 3, 'Вторник': 3,
                'Wednesday': 4, 'Среда': 4,
                'Thursday': 5, 'Четверг': 5,
                'Friday': 6, 'Пятница': 6,
                'Saturday': 7, 'Суббота': 7,
                'Sunday': 1, 'Воскресенье': 1,
            }
            weekday_number = weekdays_dict.get(weekday_name)
            if weekday_number is None:
                return Response(
                    {"error": f"Invalid weekday: {weekday_name}"},
                status=status.HTTP_400_BAD_REQUEST)

            queryset = queryset.annotate(weekday=ExtractWeekDay('deadline')).filter(weekday=weekday_number)

        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_task_by_id(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(['GET'])
def task_statistics(request):
    total_tasks = Task.objects.all().count()

    from collections import Counter
    status_amount = Task.objects.values_list('status', flat=True)
    status_count = Counter(status_amount)

    status_labels = dict(Task._meta.get_field('status').choices)
    status_labels_count = {status_labels.get(k, k): v for k, v in status_count.items()}

    overdue = Task.objects.filter(deadline__lt=now().date()).exclude(status='D').count()

    return Response({
        'total_tasks': total_tasks,
        'by_status': status_labels_count,
        'overdue': overdue
    })


class SubTaskListCreateView(APIView):
    class SubTaskPagination(PageNumberPagination):
        page_size = 5

    def get(self, request):
        queryset = SubTask.objects.all().order_by('-created_at')

        task_title = request.query_params.get('task')
        status = request.query_params.get('status')

        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)
        if status:
            queryset = queryset.filter(status=status)

        paginator = self.SubTaskPagination()
        paginated_qs = paginator.paginate_queryset(queryset, request, view=self)
        serializer = SubTaskSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SubTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return None

    def get(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)