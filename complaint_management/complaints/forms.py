from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import User, Employee, Customer, Product, Complaint, ComplaintRemark

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

class EmployeeForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[RegexValidator(r'^[0-9]{10,15}$', 'Enter a valid phone number (10-15 digits).')]
    )

    class Meta:
        model = Employee
        fields = ['phone', 'designation', 'salary', 'address']
        widgets = {
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if self.instance.pk:
            # Editing: exclude current user
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError('This email address is already in use.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if self.instance.pk and not password:
            # Editing and not changing password
            return password
        if password and len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if password and (not any(c.isdigit() for c in password) or not any(c.isalpha() for c in password)):
            raise ValidationError('Password must contain both letters and numbers.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        phone = cleaned_data.get('phone')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        # Phone validation (already handled by RegexValidator, but double-check)
        if phone and (not phone.isdigit() or not (10 <= len(phone) <= 15)):
            self.add_error('phone', 'Enter a valid phone number (10-15 digits).')

        return cleaned_data

    def save(self, commit=True):
        employee = super().save(commit=False)
        # Create or update user
        if self.instance.pk:  # Updating existing employee
            user = self.instance.user
            user.username = self.cleaned_data['username']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            if self.cleaned_data.get('password'):
                user.set_password(self.cleaned_data['password'])
            user.save()
        else:  # Creating new employee
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                role='employee'
            )
            employee.user = user
        if commit:
            employee.save()
        return employee

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'contact_number', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'tax']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'tax': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['customer', 'product', 'complaint_level', 'description']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'complaint_level': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ComplaintRemarkForm(forms.ModelForm):
    class Meta:
        model = ComplaintRemark
        fields = ['remark']
        widgets = {
            'remark': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your remark or work report...'
            }),
        } 