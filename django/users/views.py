from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from home.settings import PROJECT_NAME, PROJECT_YEAR
from .forms import UserSignIn, UserSignUp

# Sign In View
def signin(request):
    if request.method == 'POST':
        signin_form = UserSignIn(request, data=request.POST)  # Get POST data
        if signin_form.is_valid():  # Validate the form
            username = signin_form.cleaned_data.get('username')
            password = signin_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(f'{user.first_name.capitalize()} logged in.')
                login(request, user)
                return redirect('secret_santa')
        else:
            print(f'Form Errors: {signin_form.errors}')  # Add this to debug the form errors
            signin_form = UserSignIn(request.POST)  # Reinitialize with POST data
    else:
        signin_form = UserSignIn()  # Initialize an empty form for GET requests

    context = {
        'project_name': PROJECT_NAME,
        'project_year': PROJECT_YEAR,
        'signin_form': signin_form,
    }
    return render(request, 'users/signin.html', context)

# Sign Up View
def signup(request):
    if request.method == 'POST':
        signup_form = UserSignUp(request.POST)  # Get POST data
        if signup_form.is_valid():  # Validate the form
            user = signup_form.save()  # Save the user to the database
            login(request, user)  # Log the user in immediately after they sign up
            return redirect('secret_santa')  # Redirect to home or dashboard page after signup
    else:
        signup_form = UserSignUp()  # Initialize an empty form for GET requests

    context = {
        'project_name': PROJECT_NAME,
        'project_year': PROJECT_YEAR,
        'signup_form': signup_form,
    }
    return render(request, 'users/signup.html', context)

def logout_view(request):
    print(f'{request.user.first_name.capitalize()} logged out.')
    logout(request)
    return redirect('signin')
