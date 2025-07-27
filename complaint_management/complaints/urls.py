from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin Dashboard
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Employee Management
    path('admin_employees/', views.employee_list, name='employee_list'),
    path('admin_employees/create/', views.employee_create, name='employee_create'),
    path('admin_employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('admin_employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    
    # Customer Management
    path('admin_customers/', views.customer_list, name='customer_list'),
    path('admin_customers/create/', views.customer_create, name='customer_create'),
    path('admin_customers/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('admin_customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    
    # Product Management
    path('admin_products/', views.product_list, name='product_list'),
    path('admin_products/create/', views.product_create, name='product_create'),
    path('admin_products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('admin_products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Complaint Management
    path('admin_complaints/', views.complaint_list, name='complaint_list'),
    path('admin_complaints/create/', views.complaint_create, name='complaint_create'),
    path('admin_complaints/<int:pk>/edit/', views.complaint_edit, name='complaint_edit'),
    path('admin_complaints/<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('admin_complaints/<int:pk>/assign/', views.assign_complaint, name='assign_complaint'),
    
    # Employee Dashboard
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/complaints/assigned/', views.assigned_complaints, name='assigned_complaints'),
    path('employee/complaints/unassigned/', views.unassigned_complaints, name='unassigned_complaints'),
    path('employee/complaints/<int:pk>/assign/', views.assign_to_me, name='assign_to_me'),
    path('employee/complaints/<int:pk>/', views.complaint_detail_employee, name='complaint_detail_employee'),
    path('employee/complaints/<int:pk>/status/', views.update_complaint_status, name='update_complaint_status'),
    
    # API
    path('api/save-location/', views.save_location, name='save_location'),
] 