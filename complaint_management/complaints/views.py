from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
from django.contrib.auth.models import User
from .models import User as CustomUser, Employee, Customer, Product, Complaint, ComplaintRemark
from .forms import LoginForm, EmployeeForm, CustomerForm, ProductForm, ComplaintForm, ComplaintRemarkForm
import json

# -------------------------------
# Authentication Views
# -------------------------------

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('employee_dashboard')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# -------------------------------
# Admin Views
# -------------------------------

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_employees = Employee.objects.count()
    total_customers = Customer.objects.count()
    total_products = Product.objects.count()
    total_complaints = Complaint.objects.count()
    pending_complaints = Complaint.objects.filter(status='Pending').count()
    closed_complaints = Complaint.objects.filter(status='Closed').count()
    
    context = {
        'total_employees': total_employees,
        'total_customers': total_customers,
        'total_products': total_products,
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'closed_complaints': closed_complaints,
    }
    return render(request, 'admin_section/dashboard.html', context)

# Employee Management
@login_required
@user_passes_test(is_admin)
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'admin_section/employee_list.html', {'employees': employees})

@login_required
@user_passes_test(is_admin)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, 'Employee created successfully')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'admin_section/employee_form.html', {'form': form, 'title': 'Create Employee'})

@login_required
@user_passes_test(is_admin)
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully')
            return redirect('employee_list')
    else:
        # Populate form with existing user data
        form = EmployeeForm(instance=employee)
        form.fields['username'].initial = employee.user.username
        form.fields['first_name'].initial = employee.user.first_name
        form.fields['last_name'].initial = employee.user.last_name
        form.fields['email'].initial = employee.user.email
    return render(request, 'admin_section/employee_form.html', {'form': form, 'title': 'Edit Employee'})

@login_required
@user_passes_test(is_admin)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully')
        return redirect('employee_list')
    return render(request, 'admin_section/employee_confirm_delete.html', {'employee': employee})

# Customer Management
@login_required
@user_passes_test(is_admin)
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'admin_section/customer_list.html', {'customers': customers})

@login_required
@user_passes_test(is_admin)
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'admin_section/customer_form.html', {'form': form, 'title': 'Create Customer'})

@login_required
@user_passes_test(is_admin)
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully')
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'admin_section/customer_form.html', {'form': form, 'title': 'Edit Customer'})

@login_required
@user_passes_test(is_admin)
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully')
        return redirect('customer_list')
    return render(request, 'admin_section/customer_confirm_delete.html', {'customer': customer})

# Product Management
@login_required
@user_passes_test(is_admin)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'admin_section/product_list.html', {'products': products})

@login_required
@user_passes_test(is_admin)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'admin_section/product_form.html', {'form': form, 'title': 'Create Product'})

@login_required
@user_passes_test(is_admin)
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_section/product_form.html', {'form': form, 'title': 'Edit Product'})

@login_required
@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully')
        return redirect('product_list')
    return render(request, 'admin_section/product_confirm_delete.html', {'product': product})

# Complaint Management
@login_required
@user_passes_test(is_admin)
def complaint_list(request):
    complaints = Complaint.objects.all().order_by('-created_at')

    # Get filter values from GET request
    assigned_to = request.GET.get('assigned_to')
    status = request.GET.get('status')
    date = request.GET.get('date')
    product = request.GET.get('product')
    customer = request.GET.get('customer')

    if assigned_to:
        complaints = complaints.filter(assigned_to__id=assigned_to)
    if status:
        complaints = complaints.filter(status=status)
    if date:
        complaints = complaints.filter(created_at__date=date)
    if product:
        complaints = complaints.filter(product__id=product)
    if customer:
        complaints = complaints.filter(customer__id=customer)

    # For filter dropdowns
    employees = Employee.objects.all()
    products = Product.objects.all()
    customers = Customer.objects.all()

    return render(request, 'admin_section/complaint_list.html', {
        'complaints': complaints,
        'employees': employees,
        'products': products,
        'customers': customers,
    })

@login_required
@user_passes_test(is_admin)
def complaint_create(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.created_by = request.user
            complaint.save()
            messages.success(request, 'Complaint registered successfully')
            return redirect('complaint_list')
    else:
        form = ComplaintForm()
    return render(request, 'admin_section/complaint_form.html', {'form': form, 'title': 'Register Complaint'})

@login_required
@user_passes_test(is_admin)
def complaint_edit(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, 'Complaint updated successfully')
            return redirect('complaint_list')
    else:
        form = ComplaintForm(instance=complaint)
    return render(request, 'admin_section/complaint_form.html', {'form': form, 'title': 'Edit Complaint'})

@login_required
@user_passes_test(is_admin)
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    remarks = complaint.remarks.all().order_by('-timestamp')
    return render(request, 'admin_section/complaint_detail.html', {'complaint': complaint, 'remarks': remarks})

@login_required
@user_passes_test(is_admin)
def assign_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        if employee_id:
            employee = get_object_or_404(Employee, pk=employee_id)
            complaint.assigned_to = employee
            complaint.save()
            messages.success(request, f'Complaint assigned to {employee.user.get_full_name()}')
        return redirect('complaint_detail', pk=pk)
    
    employees = Employee.objects.all()
    return render(request, 'admin_section/assign_complaint.html', {'complaint': complaint, 'employees': employees})

# -------------------------------
# Employee Views
# -------------------------------

def is_employee(user):
    return user.is_authenticated and user.role == 'employee'

@login_required
@user_passes_test(is_employee)
def employee_dashboard(request):
    try:
        employee = request.user.employee_profile
        assigned_complaints = Complaint.objects.filter(assigned_to=employee).count()
        unassigned_complaints = Complaint.objects.filter(assigned_to__isnull=True).count()
        
        context = {
            'assigned_complaints': assigned_complaints,
            'unassigned_complaints': unassigned_complaints,
        }
    except Employee.DoesNotExist:
        context = {
            'assigned_complaints': 0,
            'unassigned_complaints': 0,
        }
    
    return render(request, 'employees/dashboard.html', context)

@login_required
@user_passes_test(is_employee)
def assigned_complaints(request):
    try:
        employee = request.user.employee_profile
        complaints = Complaint.objects.filter(assigned_to=employee).order_by('-created_at')
        
        # Get filter values from GET request
        status = request.GET.get('status')
        date = request.GET.get('date')
        search = request.GET.get('search')

        # Apply filters if present
        if status:
            complaints = complaints.filter(status=status)
        if date:
            complaints = complaints.filter(created_at__date=date)
        if search:
            complaints = complaints.filter(description__icontains=search)
    except Employee.DoesNotExist:
        complaints = []

    return render(request, 'employees/assigned_complaints.html', {'complaints': complaints})

@login_required
@user_passes_test(is_employee)
def unassigned_complaints(request):
    complaints = Complaint.objects.filter(assigned_to__isnull=True).order_by('-created_at')
    return render(request, 'employees/unassigned_complaints.html', {'complaints': complaints})

@login_required
@user_passes_test(is_employee)
def assign_to_me(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    try:
        employee = request.user.employee_profile
        complaint.assigned_to = employee
        complaint.save()
        messages.success(request, 'Complaint assigned to you successfully')
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found')
    
    return redirect('unassigned_complaints')

@login_required
@user_passes_test(is_employee)
def complaint_detail_employee(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    remarks = complaint.remarks.all().order_by('-timestamp')
    
    if request.method == 'POST':
        form = ComplaintRemarkForm(request.POST)
        if form.is_valid():
            remark = form.save(commit=False)
            remark.complaint = complaint
            remark.employee = request.user.employee_profile
            remark.save()
            messages.success(request, 'Remark added successfully')
            return redirect('complaint_detail_employee', pk=pk)
    else:
        form = ComplaintRemarkForm()
    
    return render(request, 'employees/complaint_detail.html', {
        'complaint': complaint, 
        'remarks': remarks, 
        'form': form
    })

@login_required
@user_passes_test(is_employee)
def update_complaint_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['Pending', 'Closed', 'Not Closed']:
            complaint.status = status
            complaint.save()
            messages.success(request, 'Status updated successfully')
    
    return redirect('complaint_detail_employee', pk=pk)

# -------------------------------
# API Views for AJAX
# -------------------------------

@csrf_exempt
def save_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        complaint_id = data.get('complaint_id')
        lat = data.get('lat')
        lng = data.get('lng')
        
        if complaint_id and lat and lng:
            complaint = get_object_or_404(Complaint, pk=complaint_id)
            complaint.location_lat = lat
            complaint.location_lng = lng
            complaint.save()
            return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'})
