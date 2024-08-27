from django.contrib import admin
from .models import Reader, Author, Contract, ContractVerified, ContactVerified, UserLog

@admin.register(Reader)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_darkmode', 'is_delete', 'delete_date', 'created_date', 'updated_date', 'slug')
    list_filter = ('is_darkmode', 'is_delete', 'created_date', 'updated_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')
    readonly_fields = ('created_date', 'updated_date', 'slug')

@admin.register(Author)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'role', 'is_darkmode', 'is_delete', 'delete_date', 'created_date', 'updated_date', 'slug')
    list_filter = ('role', 'is_darkmode', 'is_delete', 'created_date', 'updated_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone', 'role')
    readonly_fields = ('created_date', 'updated_date', 'slug')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_delete', 'delete_date', 'created_date', 'updated_date', 'slug')
    list_filter = ('is_delete', 'created_date', 'updated_date')
    search_fields = ('title',)
    readonly_fields = ('created_date', 'updated_date', 'slug')

@admin.register(ContractVerified)
class ContractVerifiedAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_date', 'updated_date')
    list_filter = ('created_date', 'updated_date')
    search_fields = ('customer__user__username', 'customer__user__first_name', 'customer__user__last_name')
    readonly_fields = ('created_date', 'updated_date')

@admin.register(ContactVerified)
class ContactVerifiedAdmin(admin.ModelAdmin):
    list_display = ('customer', 'is_phone', 'is_mail', 'is_delete', 'delete_date', 'created_date', 'updated_date')
    list_filter = ('is_phone', 'is_mail', 'is_delete', 'created_date', 'updated_date')
    search_fields = ('customer__user__username', 'customer__user__first_name', 'customer__user__last_name')
    readonly_fields = ('created_date', 'updated_date')

@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'action')
    readonly_fields = ('created_date',)
