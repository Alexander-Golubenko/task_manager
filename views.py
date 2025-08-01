from django.db.models.functions import ExtractWeekDay
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import  Response
from rest_framework import filters, status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import *
from django.utils.timezone import now
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from .permissions import ReadOnlyOrAuthenticated, IsOwnerOrAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class TaskListCreateAPIView(ListCreateAPIView):
    """
    get:
    Return a list of tasks with optional filters:
    - ?status=<status_value>
    - ?deadline=<YYYY-MM-DD>
    - ?search=<text> (matches title and description)
    - ?ordering=created_at or -created_at
    - ?weekday=<Weekday name> (English or Russian, e.g. 'Monday' or 'Понедельник')

    post:
    Create a new task.
    """
    permission_classes = (ReadOnlyOrAuthenticated,)

    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Task.objects.all()
        weekday_name = self.request.query_params.get('weekday')

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
                raise ValidationError({'weekday': f'Invalid weekday: {weekday_name}'})
            queryset = queryset.annotate(weekday=ExtractWeekDay('deadline')).filter(weekday=weekday_number)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

    permission_classes = (IsOwnerOrAdminOrReadOnly,)

@api_view(['GET'])
@permission_classes([IsAdminUser])
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


class SubTaskListCreateAPIView(ListCreateAPIView):
    """
    get:
    Return a list of subtasks with optional filters:
    - ?status=<status_value>
    - ?deadline=<YYYY-MM-DD>
    - ?search=<text> (matches title and description)
    - ?ordering=created_at or -created_at
    - ?task=<partial task title> (filters by related task title)

    post:
    Create a new subtask.
    """
    serializer_class = SubTaskCreateSerializer
    permission_classes = (ReadOnlyOrAuthenticated,)

    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = SubTask.objects.all()
        task_title = self.request.query_params.get('task')
        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubTaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    permission_classes = (IsOwnerOrAdminOrReadOnly,)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        task_count = category.task_set.count()
        return Response({'category': category.name, 'task_count': task_count})


class MyTasksAPIView(ListCreateAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class MySubTasksAPIView(ListCreateAPIView):
    serializer_class = SubTaskCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)

class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Logout failed."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)