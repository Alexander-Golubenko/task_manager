from django.contrib import admin
from HW_8.models import Category, Task, SubTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'created_at', 'deadline')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'description')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'deadline')
