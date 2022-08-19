from django.dispatch import receiver
from wagtail.core.signals import page_published

from .models import SimplePage


@receiver(page_published, sender=SimplePage)
def send_grpc_on_save(sender, **kwargs):
    """TODO call telegram and others to publish this super page"""
