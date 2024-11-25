from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

style = 'bg-zinc-50 border border-zinc-300 text-zinc-900 text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2.5  dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white dark:focus:ring-green-500 dark:focus:border-green-500'

class UserSignUp(UserCreationForm):
    first_name = forms.CharField(label='First Name', max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'John',
        'autofocus': True,
        'class': style
        }))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Doe',
        'class': style
    }))
    username = forms.CharField(label='Username', max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'johndoe',
        'autofocus': False,
        'class': style,
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'example@example.com',
        'class': style,
    }))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'placeholder': '••••••••',
        'class': style
    }))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        'placeholder': '••••••••',
        'class': style
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

class UserSignIn(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'autofocus': False,
        'class': style
        }))
    
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'placeholder': '••••••••',
        'class': style
    }))
    # username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']
