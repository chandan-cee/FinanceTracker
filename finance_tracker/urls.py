"""
URL configuration for finance_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from transactions.views import home, add_transaction, view_transactions, transaction_chart, exit_app, all_transactions

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),  # Home page with 4 buttons
    path("add/", add_transaction, name="add_transaction"),
    path("view/", view_transactions, name="view_transactions"),
    path("chart/", transaction_chart, name="transaction_chart"),
    path("exit/", exit_app, name="exit_app"),
    path("all-transactions/", all_transactions, name="all_transactions"),
]
