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
    session_url = models.URLField(blank=True, null=True)
    session_id = models.CharField(max_length=60, blank=True, null=True)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.money_to_pay = self.calculate_total_borrowing_amount()
        super().save(*args, **kwargs)

    def calculate_total_borrowing_amount(self):
        borrowing_days = (self.borrowing.expected_return_date - self.borrowing.borrow_date).days
        total_amount = self.borrowing.book.daily_fee * borrowing_days
        return total_amount

    def __str__(self) -> str:
        return (
            f"|Status: {self.status} | "
            f"Type: {self.type} | "
            f"Money to pay: {self.money_to_pay}|"
        )
