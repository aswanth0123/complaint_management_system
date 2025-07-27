from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Employee, Customer, Product, Complaint, ComplaintRemark

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'designation', 'phone', 'salary')
    list_filter = ('designation',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'designation')
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Employee Details', {
            'fields': ('phone', 'designation', 'salary', 'address')
        }),
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number', 'email')
    search_fields = ('name', 'contact_number', 'email')
    list_filter = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'tax')
    search_fields = ('name',)
    list_filter = ('tax',)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'complaint_level', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'complaint_level', 'created_at')
    search_fields = ('customer__name', 'product__name', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Complaint Information', {
            'fields': ('customer', 'product', 'complaint_level', 'description')
        }),
        ('Location', {
            'fields': ('location_lat', 'location_lng')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'assigned_to', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(ComplaintRemark)
class ComplaintRemarkAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'employee', 'timestamp')
    list_filter = ('timestamp', 'employee')
    search_fields = ('complaint__customer__name', 'employee__user__username')
    readonly_fields = ('timestamp',)
