from django.db import models
from django.contrib.auth.models import AbstractUser

# -------------------------------
# 1. Custom User Model
# -------------------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


# -------------------------------
# 2. Employee Profile
# -------------------------------
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    phone = models.CharField(max_length=15)
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.designation}"


# -------------------------------
# 3. Customer
# -------------------------------
class Customer(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name


# -------------------------------
# 4. Product
# -------------------------------
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2)  # in percent

    def __str__(self):
        return self.name

    def total_price(self):
        return float(self.price) + (float(self.price) * float(self.tax) / 100)


# -------------------------------
# 5. Complaint
# -------------------------------
class Complaint(models.Model):
    COMPLAINT_LEVEL_CHOICES = (
        ('Level 1', 'Level 1'),
        ('Level 2', 'Level 2'),
        ('Level 3', 'Level 3'),
    )

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Closed', 'Closed'),
        ('Not Closed', 'Not Closed'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    complaint_level = models.CharField(max_length=10, choices=COMPLAINT_LEVEL_CHOICES)
    description = models.TextField()
    location_lat = models.FloatField(blank=True, null=True)
    location_lng = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_complaints')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint #{self.id} - {self.customer.name}"


# -------------------------------
# 6. Complaint Remark / Work Report
# -------------------------------
class ComplaintRemark(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='remarks')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    remark = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Remark by {self.employee.user.username} on Complaint #{self.complaint.id}"
