from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from borrowings.utils import send_telegram_notification


@receiver(post_save, sender="borrowings.Borrowing")
def handle_borrowing_creation(instance, created, **kwargs):
    if created:
        send_telegram_notification(instance)
