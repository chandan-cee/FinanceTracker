from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum
from .models import Transaction
from .forms import TransactionForm
import matplotlib.pyplot as plt
import io
import urllib, base64
import sys  # Needed for exit function
import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend


# Home page with buttons
def home(request):
    return render(request, "transactions/home.html")

# 1️⃣ Add Transaction Page
def add_transaction(request):
    form = TransactionForm()
    
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")  # Redirect back to home page after saving

    return render(request, "transactions/add_transaction.html", {"form": form})

# 2️⃣ View Transactions & Summary
def view_transactions(request):
    transactions = []
    total_income = total_expense = net_savings = 0

    if request.method == "POST":
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        
        transactions = Transaction.objects.filter(date__range=[start_date, end_date])
        total_income = transactions.filter(category="Income").aggregate(Sum("amount"))["amount__sum"] or 0
        total_expense = transactions.filter(category="Expense").aggregate(Sum("amount"))["amount__sum"] or 0
        net_savings = total_income - total_expense

    return render(request, "transactions/view_transactions.html", {
        "transactions": transactions,
        "total_income": total_income,
        "total_expense": total_expense,
        "net_savings": net_savings,
    })

# 3️⃣ Plot Graph
def transaction_chart(request):
    transactions = Transaction.objects.all()
    income = transactions.filter(category="Income").aggregate(total=Sum("amount"))["total"] or 0
    expense = transactions.filter(category="Expense").aggregate(total=Sum("amount"))["total"] or 0

    labels = ["Income", "Expense"]
    values = [income, expense]

    plt.figure(figsize=(5, 5))
    plt.pie(values, labels=labels, autopct="%1.1f%%", colors=["green", "red"])
    plt.title("Income vs Expense")

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return render(request, "transactions/chart.html", {"chart": image_base64})

# 4️⃣ Exit Application
def exit_app(request):
    sys.exit("Exiting Finance Tracker...")


def all_transactions(request):
    transactions = Transaction.objects.all().order_by("-date")  # Fetch all transactions
    return render(request, "transactions/all_transactions.html", {"transactions": transactions})
