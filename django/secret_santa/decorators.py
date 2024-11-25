from django.shortcuts import redirect
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Group

# def user_belongs_to_group(redirect_url='home'):
#     """
#     A decorator that checks if a user is part of any group. If not, they are redirected to a specific URL.
#     """
#     def decorator(view_func):
#         @wraps(view_func)
#         @login_required  # Ensure the user is logged in first
#         def _wrapped_view(request, *args, **kwargs):
#             # Check if the user is part of any group
#             if not Group.objects.filter(members=request.user).exists():
#                 # If not part of any group, redirect to a specified URL
#                 return redirect(redirect_url)
#             return view_func(request, *args, **kwargs)
#         return _wrapped_view
#     return decorator

def user_belongs_to_group(redirect_url='home'):
    """
    A decorator that checks if a user is part of any group. If not, they are redirected to a specific URL.
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required  # Ensure the user is logged in first
        def _wrapped_view(request, group_code, *args, **kwargs):
            # Check if the user is part of the specified group
            if not Group.objects.filter(code=group_code).filter(members=request.user).exists():
                # If not part of any group, redirect to a specified URL
                return redirect(redirect_url)
            return view_func(request, group_code, *args, **kwargs)
        return _wrapped_view
    return decorator

def user_is_group_admin(redirect_url='home'):
    """
    A decorator that checks if a user is the admin of the group. If not, they are redirected to a specific URL.
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required  # Ensure the user is logged in first
        def _wrapped_view(request, group_code, *args, **kwargs):
            # Check if the user is part of the specified group
            # if not Group.objects.filter(code=group_code).filter(members=request.user).exists():
            #     return redirect(redirect_url)

            if request.user == Group.objects.get(code=group_code).admin:
                print(f'The user {request.user} is the admin of {group_code}')
                return view_func(request, group_code, *args, **kwargs)
            else:
                print(f'The user {request.user} is the NOT admin of {group_code}')
                return redirect(redirect_url)
        return _wrapped_view
    return decorator
