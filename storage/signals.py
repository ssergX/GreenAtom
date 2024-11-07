from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Organization


@receiver(post_save, sender=Organization)
@receiver(post_delete, sender=Organization)
def update_storage_current_waste(sender, instance, **kwargs):

    if instance.storage:
        instance.storage.update_current_waste()
