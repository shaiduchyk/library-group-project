from django.db.models.signals import post_save
from django.dispatch import receiver
from borrowings.utils import send_telegram_notification


@receiver(post_save, sender="borrowings.Borrowing")
def handle_borrowing_creation(instance, created, **kwargs):
    if created:
        message = (f"New borrowing for book: {instance.book.title},"
                   f" Expected return date: {instance.expected_return_date}")
        send_telegram_notification(message)


@receiver(post_save, sender="payment_system.FinePayment")
def handle_fine_payment_creation(instance, created, **kwargs):
    if created:
        payment_date = instance.payment_date.strftime("%Y-%m-%d")
        message = (f"You have to pay ${instance.money_to_pay} for book "
                   f"{instance.borrowing.book.title} overdue until {payment_date}")
        send_telegram_notification(message)
