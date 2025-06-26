from rest_framework.decorators import api_view
from rest_framework.response import  Response
from rest_framework import status
from .models import  Task
from .serializers import TaskSerializer
from django.utils.timezone import now

@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_tasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
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