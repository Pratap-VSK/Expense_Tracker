from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal
from .models import Transaction, Category
from .forms import TransactionForm
import json

@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)

    total_income = transactions.filter(category__category_type='INCOME').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_expense = transactions.filter(category__category_type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    balance = total_income - total_expense

    recent_transactions = transactions.order_by('-date')[:5]

    expenses_data = transactions.filter(category__category_type='EXPENSE') \
                                .values('category__name') \
                                .annotate(total=Sum('amount'))

    chart_labels = [item['category__name'] or 'Uncategorized' for item in expenses_data]
    chart_data = [float(item['total']) for item in expenses_data]

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'recent_transactions': recent_transactions,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'tracker/dashboard.html', context)

# [CREATE] Add New Entry
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  # Data Isolation: User link kar diya
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'tracker/add_expenses.html', {'form': form})

# [UPDATE] Edit Entry
@login_required
def edit_expense(request, pk):
    # Ensure user sirf apna hi data edit kar sake
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'tracker/edit_expenses.html', {'form': form})

# [DELETE] Remove Entry
@login_required
def delete_expense(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('dashboard')
    return render(request, 'tracker/confirm_delete.html', {'transaction': transaction})