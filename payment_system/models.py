from django.db import models

from borrowings.models import Borrowing


class PaymentStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PAID = "PAID", "Paid"


class PaymentType(models.TextChoices):
    PAYMENT = "PAYMENT", "Payment"
    FINE = "FINE", "Fine"


class Payment(models.Model):
    status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    type = models.CharField(
        max_length=10,
        choices=PaymentType.choices,
        default=PaymentType.PAYMENT
    )
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField()
    session_id = models.CharField(max_length=60)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return (
            f"|Status: {self.status} | "
            f"Type: {self.type} | "
            f"Money to pay: {self.money_to_pay}|"
        )
