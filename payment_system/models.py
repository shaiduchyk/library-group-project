from django.db import models


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
    borrowing = models.ForeignKey("borrowings.Borrowing", on_delete=models.CASCADE)
    session_url = models.URLField(blank=True, null=True)
    session_id = models.CharField(max_length=60, blank=True, null=True)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return (
            f"|Status: {self.status} | "
            f"Type: {self.type} | "
            f"Money to pay: {self.money_to_pay}|"
        )


class FinePayment(models.Model):
    borrowing = models.ForeignKey("borrowings.Borrowing", on_delete=models.CASCADE)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fine payment for Borrowing {self.borrowing_id}"
