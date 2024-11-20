from django.shortcuts import render, redirect
from home.settings import PROJECT_NAME, PROJECT_YEAR
from django.contrib.auth.decorators import login_required
from .forms import GroupCreationForm, GroupJoinForm, GiftPreferenceForm
from .models import Group, GiftPreference
from django.contrib import messages

# Create your views here.

def home(request):
    context = {
        'project_name': PROJECT_NAME,
        'project_year': PROJECT_YEAR,
    }
    return render(request, 'secret_santa/home.html', context)

@login_required
def secret_santa(request):
    if request.method == 'POST':
        # Check if the user is creating a new group
        if 'create_group' in request.POST:
            group_form = GroupCreationForm(request.POST)
            join_form = GroupJoinForm()
            if group_form.is_valid():
                group = group_form.save(commit=False)
                group.save()  # Save the group to the database
                group.add_user(request.user)
                # Add the user as a member of the group immediately with default preferences
                GiftPreference.objects.create(user=request.user, group=group, gift_list='', max_price=0.00)

                # Notify user of successful group creation
                messages.success(request, f'Group "{group.name}" created successfully! You can share the group code: {group.code}')
                return redirect('group_view')  # Redirect to the same page or another view after group creation

        # Check if the user is joining an existing group
        elif 'join_group' in request.POST:
            group_form = GroupCreationForm()
            join_form = GroupJoinForm(request.POST)
            if join_form.is_valid():
                code = join_form.cleaned_data['code']
                try:
                    # Fetch the group by the code
                    group = Group.objects.get(code=code)
                    
                    # Add the user to the group using the custom add_user method
                    group.add_user(request.user)

                    # Add default gift preferences for the user
                    GiftPreference.objects.create(user=request.user, group=group, gift_list='', max_price=0.00)

                    # Notify user of successful group joining
                    messages.success(request, f'You have successfully joined the group "{group.name}"!')
                    return redirect('group_view')  # Redirect after joining the group

                except Group.DoesNotExist:
                    # Handle invalid group code
                    messages.error(request, 'Invalid group code. Please try again.')
                    return redirect('secret_santa')  # Redirect back to try again

    else:
        group_form = GroupCreationForm()
        join_form = GroupJoinForm()
    
    group = Group.objects.filter(members=request.user)
    # print('group', group)
    context = {
        'project_name': PROJECT_NAME,  # Set the project name
        'project_year': PROJECT_YEAR,  # Set the project year (or use dynamic values)
        'group_form': group_form,
        'group': group,
        'join_form': join_form,
    }
    return render(request, 'secret_santa/secret_santa.html', context)

@login_required
def group_view(request):
    # Get the group the logged-in user is part of
    try:
        group = Group.objects.filter(members=request.user)
        gift_preference = GiftPreference.objects.filter(user=request.user)
        group = gift_preference.group
        # Get the list of members in this group
        members = group.members.all()
        
        # Check if the user has a gift preference already
        if request.method == 'POST':
            form = GiftPreferenceForm(request.POST, instance=gift_preference)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your gift preferences have been updated successfully!')
                return redirect('group_view')  # Redirect to the same page after saving the form
        else:
            form = GiftPreferenceForm(instance=gift_preference)

    except GiftPreference.DoesNotExist:
        messages.error(request, 'You are not part of any group.')
        return redirect('secret_santa')  # Redirect if the user is not part of any group
    
    context = {
        'project_name': PROJECT_NAME,
        'project_year': PROJECT_YEAR,
        'group': group,
        'members': members,
        'gift_preference_form': form,
        # 'gift_preferences': gift_preferences,
    }
    return render(request, 'secret_santa/group_view.html', context)
