from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from complaints.models import User, Employee, Customer, Product

User = get_user_model()

class Command(BaseCommand):
    help = 'Set up initial data for the complaint management system'

    def handle(self, *args, **options):
        self.stdout.write('Setting up initial data...')
        
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='admin',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        
        # Create employee users
        employees_data = [
            {
                'username': 'employee1',
                'email': 'employee1@example.com',
                'password': 'employee123',
                'first_name': 'John',
                'last_name': 'Doe',
                'role': 'employee',
                'phone': '+1234567890',
                'designation': 'Field Engineer',
                'salary': 50000.00,
                'address': '123 Main St, City, State'
            },
            {
                'username': 'employee2',
                'email': 'employee2@example.com',
                'password': 'employee123',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'role': 'employee',
                'phone': '+1234567891',
                'designation': 'Technical Support',
                'salary': 45000.00,
                'address': '456 Oak Ave, City, State'
            }
        ]
        
        for emp_data in employees_data:
            if not User.objects.filter(username=emp_data['username']).exists():
                user = User.objects.create_user(
                    username=emp_data['username'],
                    email=emp_data['email'],
                    password=emp_data['password'],
                    first_name=emp_data['first_name'],
                    last_name=emp_data['last_name'],
                    role=emp_data['role']
                )
                
                Employee.objects.create(
                    user=user,
                    phone=emp_data['phone'],
                    designation=emp_data['designation'],
                    salary=emp_data['salary'],
                    address=emp_data['address']
                )
                self.stdout.write(self.style.SUCCESS(f'Created employee: {emp_data["first_name"]} {emp_data["last_name"]}'))
        
        # Create customers
        customers_data = [
            {
                'name': 'ABC Corporation',
                'contact_number': '+1987654321',
                'email': 'contact@abccorp.com',
                'address': '789 Business Blvd, Corporate City, State'
            },
            {
                'name': 'XYZ Industries',
                'contact_number': '+1987654322',
                'email': 'info@xyzindustries.com',
                'address': '321 Industrial Park, Factory Town, State'
            },
            {
                'name': 'Tech Solutions Inc',
                'contact_number': '+1987654323',
                'email': 'support@techsolutions.com',
                'address': '654 Innovation Drive, Tech City, State'
            }
        ]
        
        for cust_data in customers_data:
            if not Customer.objects.filter(name=cust_data['name']).exists():
                Customer.objects.create(**cust_data)
                self.stdout.write(self.style.SUCCESS(f'Created customer: {cust_data["name"]}'))
        
        # Create products
        products_data = [
            {
                'name': 'Premium Laptop',
                'price': 1200.00,
                'tax': 8.5
            },
            {
                'name': 'Office Printer',
                'price': 500.00,
                'tax': 7.0
            },
            {
                'name': 'Network Router',
                'price': 200.00,
                'tax': 6.5
            },
            {
                'name': 'Security Camera',
                'price': 150.00,
                'tax': 8.0
            }
        ]
        
        for prod_data in products_data:
            if not Product.objects.filter(name=prod_data['name']).exists():
                Product.objects.create(**prod_data)
                self.stdout.write(self.style.SUCCESS(f'Created product: {prod_data["name"]}'))
        
        self.stdout.write(self.style.SUCCESS('Initial data setup completed successfully!'))
        self.stdout.write('\nLogin Credentials:')
        self.stdout.write('Admin - Username: admin, Password: admin123')
        self.stdout.write('Employee 1 - Username: employee1, Password: employee123')
        self.stdout.write('Employee 2 - Username: employee2, Password: employee123') 