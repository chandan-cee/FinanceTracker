from django.db import models

# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("Income", "Income"),
        ("Expense", "Expense"),
    ]

    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.TextField()

    def __str__(self):
        return f"{self.date} - {self.category} - {self.amount}"

