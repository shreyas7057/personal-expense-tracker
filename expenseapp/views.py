from django.shortcuts import render, redirect
from .models import IncomeSource, Expense,Source
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from django.db.models import Sum
from django.http import JsonResponse
from django.db.models import Sum
from django.utils.dateparse import parse_date
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from .models import Expense
from django.db.models import Sum
import datetime

def home(request):
    user = request.user
    if user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login_user')


@login_required
def dashboard(request):
    incomes = IncomeSource.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    return render(request, 'expenseapp/dashboard.html', {
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance
    })


@login_required
def list_sources(request):
    sources = Source.objects.filter(user=request.user)
    return render(request, 'expenseapp/source_list.html', {'sources': sources})

@login_required
def add_source(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            Source.objects.create(user=request.user, name=name)
            return redirect('list_sources')
    return render(request, 'expenseapp/add_source.html')


@login_required
def edit_source(request, pk):
    source = Source.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            source.name = name
            source.save()
            return redirect('list_sources')
    return render(request, 'expenseapp/edit_source.html', {'source': source})

@login_required
def delete_source(request, pk):
    source = Source.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        source.delete()
        return redirect('list_sources')
    return render(request, 'expenseapp/delete_source.html', {'source': source})


@login_required
def add_income(request):
    sources = Source.objects.filter(user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        source_id = request.POST.get('name')
        date = request.POST.get('date') or timezone.now().date()

        if amount and source_id:
            source = Source.objects.get(id=source_id, user=request.user)
            IncomeSource.objects.create(
                user=request.user,
                amount=amount,
                source=source,
                date=date
            )
        return redirect('dashboard')
    
    return render(request, 'expenseapp/add_income.html',{'sources':sources})


@login_required
def add_expense(request):
    sources = IncomeSource.objects.filter(user=request.user)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        description = request.POST.get('description', '')
        date = request.POST.get('date') or timezone.now().date()
        source_id = request.POST.get('source')

        if amount and category and source_id:
            source = IncomeSource.objects.get(id=source_id, user=request.user)
            Expense.objects.create(
                user=request.user,
                source=source,
                category=category,
                description=description,
                amount=amount,
                date=date
            )
            return redirect('dashboard')

    return render(request, 'expenseapp/add_expense.html', {'sources': sources})


@login_required
def expense_report(request):
    expenses = Expense.objects.filter(user=request.user)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category = request.GET.get('category')

    if start_date:
        expenses = expenses.filter(date__gte=parse_date(start_date))
    if end_date:
        expenses = expenses.filter(date__lte=parse_date(end_date))
    if category:
        expenses = expenses.filter(category=category)

    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    categories = Expense.objects.filter(user=request.user).values_list('category', flat=True).distinct()

    return render(request, 'expenseapp/expense_report.html', {
        'expenses': expenses,
        'total': total,
        'start_date': start_date,
        'end_date': end_date,
        'category': category,
        'categories': categories,
    })

@login_required
def income_expense_charts(request):
    # Income by source
    income_data = (
        IncomeSource.objects.filter(user=request.user)
        .values('source__name')
        .annotate(total=Sum('amount'))
    )

    # Expense by category
    expense_data = (
        Expense.objects.filter(user=request.user)
        .values('category')
        .annotate(total=Sum('amount'))
    )

    return JsonResponse({
        'income': list(income_data),
        'expense': list(expense_data),
    })

@login_required
def chart_page(request):
    return render(request, 'expenseapp/charts.html')


@login_required
def generate_expense_pdf(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    template = get_template("expenseapp/expense_pdf_template.html")
    html = template.render({
        'expenses': expenses,
        'total': total,
        'user': request.user,
        'date': datetime.datetime.now(),
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expense_report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response
