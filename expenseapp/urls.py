from django.urls import path
from .views import add_expense,add_income,dashboard,add_source,list_sources,edit_source,delete_source,home,expense_report,income_expense_charts,chart_page

urlpatterns = [

    path('',home,name='home'),

    path('dashboard/',dashboard,name='dashboard'),
    path('add_expense/',add_expense,name='add_expense'),
    path('add_income/',add_income,name='add_income'),

    path('sources/', list_sources, name='list_sources'),
    path('sources/add/', add_source, name='add_source'),
    path('sources/edit/<int:pk>/', edit_source, name='edit_source'),
    path('sources/delete/<int:pk>/', delete_source, name='delete_source'),

    path('expense-report/', expense_report, name='expense_report'),

    path('charts/data/', income_expense_charts, name='chart_data'),
    path('charts/', chart_page, name='chart_page'),


]