from django.db import models


class Book(models.Model):
    class Covers(models.TextChoices):
        HARD = "hard" "HARD"
        SOFT = "soft" "SOFT"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=10, choices=Covers.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-title"]

    def __str__(self):
        return self.title
