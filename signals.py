from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Task


@receiver(pre_save, sender=Task)
def notify_owner_on_status_change(sender, instance: Task, **kwargs):
    if not instance.pk:
        return #new task

    try:
        old_instance = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return

    old_status = old_instance.status
    new_status = instance.status

    if old_status != new_status:
        user = instance.owner
        if user and user.email:
            subject = f'Task status changed: {instance.title}'
            message = f"New status of the task {instance.title} has been changed to {new_status}"
            send_mail(subject=subject,
                      message=message,
                      from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[user.email],
                      fail_silently=False,
                      )