from django.db import models
from books_service.models import Book

from library_drf import settings


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    @property
    def is_active(self):
        return self.actual_return_date is None

    def __str__(self):
        return (
            f"Borrow Date: {self.borrow_date}, "
            f" Expected Return Date: {self.expected_return_date}, "
            f"Actual Return Date: {self.actual_return_date}"
        )
