# Complaint Management System

A comprehensive Django-based complaint management system with role-based access control for Admin and Employee users.

## Features

### 🔐 Authentication & User Management
- **Role-based Access Control**: Separate interfaces for Admin and Employee users
- **Secure Login System**: Custom authentication with role validation
- **User Profile Management**: Complete user profile management for employees

### 👨‍💼 Admin Panel Features

#### Employee Master
- ✅ Create, view, and edit employee records
- ✅ Employee details: Name, Designation, Personal Details, Phone Number, Salary
- ✅ Complete CRUD operations for employee management

#### Customer Master
- ✅ Create, view, and edit customer information
- ✅ Customer details: Name, Contact Details, Address
- ✅ Comprehensive customer database management

#### Product Master
- ✅ Create, view, and edit product-related details
- ✅ Product information: Name, Price, Tax
- ✅ Product catalog management

#### Complaint Registration
- ✅ Register complaints with customer and product selection
- ✅ Complaint level selection (Level 1, Level 2, Level 3)
- ✅ Detailed complaint description
- ✅ **Google Maps Integration** for location capture
- ✅ Save, view, and edit complaint records
- ✅ Assign complaints to employees

### 👷 Employee Panel Features

#### Dashboard
- ✅ **Assigned Complaints Count**: Real-time count of complaints assigned to the employee
- ✅ **Unassigned Complaints Count**: Count of available complaints to assign

#### Complaint Handling
- ✅ **Assigned Complaints**: View and manage complaints assigned to the logged-in employee
- ✅ **Add Remarks/Work Reports**: Each update is stored with timestamp
- ✅ **Status Updates**: Pending, Closed, Not Closed
- ✅ **Unassigned Complaints**: View and assign complaints to self
- ✅ **"Assign to Me"** functionality for unassigned complaints

### 🎨 UI/UX Features
- ✅ **Responsive Design**: Works on desktop, tablet, and mobile devices
- ✅ **Modern UI**: Bootstrap 5 with custom styling
- ✅ **Form Validation**: Client and server-side validation
- ✅ **Error Handling**: Comprehensive error handling and user feedback
- ✅ **Logout Functionality**: Secure logout system

## Tech Stack

- **Backend**: Python Django 5.2.4
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: Django's built-in authentication system
- **Maps Integration**: Google Maps API for location services
- **Icons**: Font Awesome 6.0

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd complaint_management_system
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
```bash
cd complaint_management
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Initial Data
```bash
python manage.py setup_data
```

### Step 6: Run the Development Server
```bash
python manage.py runserver
```

### Step 7: Access the Application
Open your browser and navigate to: `http://127.0.0.1:8000`

## Default Login Credentials

### Admin User
- **Username**: admin
- **Password**: admin123
- **Role**: Admin (Full access to all features)

### Employee Users
- **Username**: employee1
- **Password**: employee123
- **Role**: Employee (Complaint handling access)

- **Username**: employee2
- **Password**: employee123
- **Role**: Employee (Complaint handling access)

## Google Maps Integration

To enable location services:

1. Get a Google Maps API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Replace `YOUR_GOOGLE_MAPS_API_KEY` in the complaint form template
3. Enable the Maps JavaScript API in your Google Cloud project

## Database Configuration

### Development (SQLite)
The system is configured to use SQLite by default for development.

### Production (PostgreSQL)
To use PostgreSQL in production, update the database settings in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'complaint_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Project Structure

```
complaint_management_system/
├── complaint_management/
│   ├── complaint_management/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── complaints/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── management/
│   │       └── commands/
│   │           └── setup_data.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   └── login.html
│   │   ├── admin_section/
│   │   │   ├── dashboard.html
│   │   │   ├── employee_list.html
│   │   │   ├── employee_form.html
│   │   │   ├── complaint_list.html
│   │   │   └── complaint_form.html
│   │   └── employees/
│   │       ├── dashboard.html
│   │       ├── complaint_detail.html
│   │       └── unassigned_complaints.html
│   ├── static/
│   ├── manage.py
│   └── db.sqlite3
└── README.md
```

## Key Features Implementation

### Role-Based Access Control
- Custom User model with role field
- Decorator-based access control
- Separate views for admin and employee functions

### Complaint Management
- Full CRUD operations for complaints
- Status tracking (Pending, Closed, Not Closed)
- Assignment system for employees
- Remark/Work report system

### Location Services
- Google Maps integration for complaint location
- AJAX-based location saving
- Interactive map interface

### Responsive Design
- Bootstrap 5 framework
- Mobile-first approach
- Modern UI components

## API Endpoints

### Authentication
- `GET/POST /` - Login page
- `GET /logout/` - Logout

### Admin Routes
- `GET /admin/dashboard/` - Admin dashboard
- `GET /admin/employees/` - Employee list
- `GET /admin/customers/` - Customer list
- `GET /admin/products/` - Product list
- `GET /admin/complaints/` - Complaint list

### Employee Routes
- `GET /employee/dashboard/` - Employee dashboard
- `GET /employee/complaints/assigned/` - Assigned complaints
- `GET /employee/complaints/unassigned/` - Unassigned complaints

### API Routes
- `POST /api/save-location/` - Save complaint location

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team.

---

**Note**: This is a comprehensive complaint management system designed for production use with proper security measures, responsive design, and modern web development practices.