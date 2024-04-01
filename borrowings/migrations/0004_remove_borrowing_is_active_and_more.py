# Generated by Django 4.1 on 2024-04-01 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("borrowings", "0003_borrowing_book_borrowing_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="borrowing",
            name="is_active",
        ),
        migrations.AlterField(
            model_name="borrowing",
            name="actual_return_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]