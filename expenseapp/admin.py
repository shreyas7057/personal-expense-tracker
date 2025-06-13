from django.contrib import admin

# Register your models here.
from .models import Expense,IncomeSource,Source

admin.site.register(Expense)
admin.site.register(IncomeSource)
admin.site.register(Source)