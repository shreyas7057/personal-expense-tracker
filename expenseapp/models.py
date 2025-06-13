from django.db import models
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

# Create your models here.

class Source(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class IncomeSource(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    source = models.ForeignKey(Source,on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.source + str(self.amount)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.ForeignKey(IncomeSource,on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"
