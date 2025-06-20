from django.db import models


STATUS_CHOICES = [
    ('N', 'New'),
    ('IP', 'In Progress'),
    ('D', 'Done'),
    ('P', 'Pending'),
    ('B', 'Blocked')
]



class Task(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title', unique_for_date='deadline')
    description = models.TextField(verbose_name='Description')
    categories = models.ManyToManyField("Category", verbose_name='Categories')
    status = models.CharField(choices=STATUS_CHOICES, default='N', max_length=15, verbose_name='Status')
    deadline = models.DateField(verbose_name='Deadline')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'task_manager_task'
        ordering = ('-created_at',)
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class SubTask(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title', unique=True)
    description = models.TextField(verbose_name='Description')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Task', related_name='subtasks')
    status = models.CharField(choices=STATUS_CHOICES, default='N', max_length=15, verbose_name='Status')
    deadline = models.DateField(verbose_name='Deadline')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ('-created_at',)
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'