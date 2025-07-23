from django.utils.timezone import  now

from rest_framework import serializers
from .models import  Task, SubTask, Category

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'deadline'
        ]


class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    # def validate_name(self, value):
    #     if Category.objects.filter(name=value).exists():
    #         raise serializers.ValidationError('Category already exists')
    #     return value

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
    class Meta:
        model = Task
        fields = '__all__'

    def validate_deadline(self, value):
        if value < now().date():
            raise serializers.ValidationError('Deadline cannot be before today')
        return value