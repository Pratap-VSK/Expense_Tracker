from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'description', 'date']
        # Widgets se hum Bootstrap ki 'form-control' class add kar rahe hain
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g., Groceries'}),
        }