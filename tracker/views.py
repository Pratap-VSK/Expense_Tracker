from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Transaction, Category
from .forms import TransactionForm

# [READ] Dashboard View
@login_required
def dashboard(request):
    # Sirf logged-in user ke transactions fetch karo
    transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-created_at')

    # Total Income aur Expense calculate karo
    incomes = transactions.filter(category__category_type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
    expenses = transactions.filter(category__category_type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = incomes - expenses

    context = {
        'transactions': transactions[:10], # Sirf latest 10 transactions table mein dikhayenge
        'total_income': incomes,
        'total_expense': expenses,
        'balance': balance,
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