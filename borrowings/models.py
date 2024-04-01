from django.db import models


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"Borrow Date: {self.borrow_date},"
            f" Expected Return Date: {self.expected_return_date},"
            f"Actual Return Date: {self.actual_return_date}"
            )
