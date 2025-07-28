from django.utils.timezone import  now
from rest_framework import serializers
from .models import  Task, SubTask, Category
from .validators import validate_deadline
from django.contrib.auth.models import  User
from django.contrib.auth.password_validation import validate_password


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'deadline',
            'owner',
        ]


class SubTaskCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    deadline = serializers.DateField(validators=[validate_deadline])

    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at', 'owner']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, obj, validated_data):
        if 'name' in validated_data:
            name = validated_data['name']
            if Category.objects.exclude(pk=obj.pk).filter(name=name).exists():
                raise serializers.ValidationError('Category already exists')
        return super().update(obj, validated_data)


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    deadline = serializers.DateField(validators=[validate_deadline])

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at', 'owner']

    def validate_deadline(self, value):
        if value < now().date():
            raise serializers.ValidationError('Deadline cannot be before today')
        return value


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # хэширование
        user.save()
        return user