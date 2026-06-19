from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    TYPE_CHOICES = (
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense')
    )
    name = models.CharField(max_length=50)
    category_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.category_type})"

class Transaction(models.Model):
    # User linkage for Data Isolation
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    # SET_NULL requires null=True in database
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        cat_name = self.category.name if self.category else "Uncategorized"
        return f"₹{self.amount} - {cat_name} on {self.date}"