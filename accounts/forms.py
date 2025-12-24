from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

TAILWIND_INPUT_CLASSES = 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all'

class AdminLoginForm(AuthenticationForm):
    """Custom login form for Admin with visual styling"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'login-input',
            'placeholder': 'Enter username (ManagerQC)',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'login-input',
            'placeholder': 'Enter password'
        })
    )

class OperatorLoginForm(AuthenticationForm):
    """Custom login form for Operator with visual styling"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'login-input',
            'placeholder': 'Enter username (OperatorQC)',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'login-input',
            'placeholder': 'Enter password'
        })
    )

class UserCreateForm(UserCreationForm):
    """Form for admin to create new users"""
    full_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'Full Name'})
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'Email'}),
            'role': forms.Select(attrs={'class': TAILWIND_INPUT_CLASSES}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = TAILWIND_INPUT_CLASSES
        self.fields['password2'].widget.attrs['class'] = TAILWIND_INPUT_CLASSES

class UserEditForm(forms.ModelForm):
    """Form for admin to edit users"""
    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'role', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
            'full_name': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
            'email': forms.EmailInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
            'role': forms.Select(attrs={'class': TAILWIND_INPUT_CLASSES}),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'}),
        }
