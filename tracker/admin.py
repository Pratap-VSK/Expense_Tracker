from django.contrib import admin
from .models import Category, Transaction
admin.site.register(Category)
admin.site.register(Transaction)
#@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'Category_type')
    list_filter = ('Category_type')
    search_fields = ('name')

#@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'category', 'date', 'user')
    list_filter = ('date', 'category', 'user')
    search_fields = ('description',)