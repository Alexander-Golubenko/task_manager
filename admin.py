from django.contrib import admin
from HW_8.models import Category, Task, SubTask




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'deadline')

    def update_status(self, request, queryset):
        queryset.update(status='Done')

    update_status.short_description = 'Update status to "Done"'
    actions = [update_status]

class SubTaskInLine(admin.StackedInline):
    model = SubTask
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'description', 'status', 'created_at', 'deadline')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'description')
    inlines = [SubTaskInLine]

    def short_title(self, obj):
        if len(obj.title) > 10:
            return obj.title[:10] + "..."
        return obj.title
    short_title.short_description = 'Title (short)'