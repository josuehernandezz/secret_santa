from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from home.settings import PROJECT_NAME, PROJECT_YEAR
from django.contrib.auth.decorators import login_required
from .forms import GroupCreationForm, GroupJoinForm, GiftPreferenceForm, DeleteUserFromGroupForm
from .models import Group, GiftPreference, Assignment
from django.contrib import messages
from django.db.models import Prefetch
from .decorators import user_belongs_to_group, user_is_group_admin
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.templatetags.static import static

# Custom
from .utils import return_members_data

# Create your views here.

# def home(request):
#     # Generate the absolute URL for the static image in your view
#     image_url = static('img/secret_santa/bg.jpg')
#     full_image_url = request.build_absolute_uri(image_url)

#     context = {
#         'project_name': PROJECT_NAME,
#         'project_year': PROJECT_YEAR,
#         'image_url': full_image_url,
#         'og_title': "Your Cool Website Title",
#         'og_description': "A short description of the page or product."
#     }
#     return render(request, 'secret_santa/home.html', context)

from django.shortcuts import render
from django.templatetags.static import static

def home(request):
    # Generate the absolute URL for the static image
    image_url = static('img/secret_santa_bg.jpg')
    full_image_url = request.build_absolute_uri(image_url)
    # Generate the absolute URL for the current page (og:url)
    full_page_url = request.build_absolute_uri(request.path)

    context = {
        'project_name': PROJECT_NAME,  # Replace with your actual project name
        'project_year': PROJECT_YEAR,  # Replace with your actual project year
        'image_url': full_image_url,
        'og_title': "Online Secret Santa Gift Exchange!",
        'og_description': "A short description of the page or product.",
        'og_url': full_page_url  # Pass the full URL of the current page
    }

    return render(request, 'secret_santa/home.html', context)

@login_required
def secret_santa(request):
    user = request.user
    if request.method == 'POST':
        # Check if the user is creating a new group
        if 'create_group' in request.POST:
            group_form = GroupCreationForm(request.POST)
            join_form = GroupJoinForm()
            if group_form.is_valid():
                group = group_form.save(commit=False)
                group.save()  # Save the group to the database
                # Add the user as an admin (and save the group after)
                group.add_admin(user)
                
                # Add the user as a member of the group
                group.add_user(user)

                # Save changes to the group (especially the admin field)
                group.save()
                # Notify user of successful group creation
                messages.success(request, f'Group "{group.name}" created successfully! You can share the group code: {group.code}.')
                messages.success(request, f'You can share the group code: {group.code}.')
                messages.success(request, f'You can also see your active groups in the navigration bar section.')
                return redirect('secret_santa')  # Redirect to the same page or another view after group creation

        # Check if the user is joining an existing group
        elif 'join_group' in request.POST:
            group_form = GroupCreationForm()
            join_form = GroupJoinForm(request.POST)
            if join_form.is_valid():
                code = join_form.cleaned_data['code']
                try:
                    # Fetch the group by the code
                    group = Group.objects.get(code=code)
                    

                    # Check if the user is in the group
                    if group.members.filter(username=user.username).exists():
                        print(f"{user.username} is in the group {group.name}")
                        messages.success(request, f'You have already joined this group!')
                    else:
                        print(f"{user.username} is not in the group {group.name}")
                        # Add the user to the group using the custom add_user method
                        group.add_user(user)

                        # Notify user of successful group joining
                        messages.success(request, f'You have successfully joined the group "{group.name}"!')

                    url = reverse('group_detail_view', args=[code])
                    return redirect(url)  # Redirect after joining the group

                except Group.DoesNotExist:
                    # Handle invalid group code
                    messages.error(request, 'Invalid group code. Please try again.')
                    return redirect('secret_santa')  # Redirect back to try again

    else:
        group_form = GroupCreationForm()
        join_form = GroupJoinForm()
    
    group = Group.objects.filter(admin=user).first() or Group.objects.filter(members=user).first()
    print(group)
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
def group_list_view(request):
    groups = Group.objects.filter(members=request.user)

    context = {
    'project_name': PROJECT_NAME,
    'project_year': PROJECT_YEAR,
    'groups': groups,
    }
    return render(request, 'secret_santa/group_list_view.html', context)

@user_belongs_to_group('secret_santa')
def group_detail_view(request, group_code):
    try:
        group = Group.objects.get(code=group_code)
    except Exception as e:
        print('An error occured in the group_detail_view, which was:', e)
        messages.error(request, f'The group code {group_code} does not exist!')
        return redirect('secret_santa')

    user = request.user
    user_is_admin = True if user == group.admin else False
    members = group.members.all()

    can_activate_secret_santa = True if (members.count() >= 3 and group.all_members_have_gift) else False

    secret_santa_is_activated = True if group.all_users_assigned_secret_santa else False

    # Check if the user has existing gift preferences for this group
    gift_preference = GiftPreference.objects.filter(group=group, user=user).first()

    # Group admin
    members_except_admin = []
    for member in members:
        if member == group.admin:
            pass
        else:
            members_except_admin.append(member)

    # Determine the group form based on whether the user is the admin
    group_form = GroupCreationForm(instance=group) if user_is_admin else None
    delete_user_from_group_form = DeleteUserFromGroupForm() if user_is_admin else None

    # Determine the gift preference form: pre-fill if the user has preferences, else create a new one
    gift_form = GiftPreferenceForm(instance=gift_preference) if gift_preference else GiftPreferenceForm()

    if request.method == 'POST':
        # Checks if the post request is updating the group form (From the admin)
        if 'name' in request.POST and group_form:
            # Handle group form submission (if the user is an admin)
            group_form = GroupCreationForm(request.POST, instance=group)
            if group_form.is_valid():
                group_form.save()
                messages.success(request, 'Group information updated successfully!')
                return redirect(reverse('group_detail_view', args=[group_code]))
        elif 'gift' in request.POST:
            # Handle gift preference form submission
            gift_form = GiftPreferenceForm(request.POST, instance=gift_preference)
            if gift_form.is_valid():
                gift_form.instance.user = user
                gift_form.instance.group = group
                gift_form.save()
                
                # Function that returns data from every group member
                members_data = return_members_data(group, members)
                
                # JsonResponse({'members': members_data})
                # Broadcast the update to all users in the same group
                broadcast_json_data(group_code, members_data)  # Pass 'true' or any data you need
                messages.success(request, 'Your gift preferences have been updated successfully!')
                return redirect(reverse('group_detail_view', args=[group_code]))

        # If the form isn't valid, add an error message
        messages.error(request, 'There was an error with your submission. Please try again.')
        return redirect(reverse('group_detail_view', args=[group_code]))
    else:
        print('member_count', members.count())
        context = {
            'project_name': PROJECT_NAME,
            'project_year': PROJECT_YEAR,
            'group': group,
            'members': members,
            'member_count': members.count(),
            'can_activate_secret_santa': can_activate_secret_santa,
            'gift_preference_form': gift_form,  # Pass the gift preference form to the template
            'secret_santa_is_activated': secret_santa_is_activated,

            # Admin forms
            'user_is_admin': user_is_admin,
            'group_form': group_form,
            'members_except_admin': members_except_admin,
            'delete_user_from_group_form': delete_user_from_group_form,
        }
        return render(request, 'secret_santa/group_detail_view.html', context)

@user_is_group_admin('secret_santa')
def remove_user_from_group(request, group_code, user_id):
    group = get_object_or_404(Group, code=group_code)
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        print('here')
        checked = request.POST.get('delete_user')
        if checked == 'on' and user in group.members.all():
            group.members.remove(user)
            messages.success(request, f"You successfully removed {user.first_name} {user.last_name} from your group.")
            return redirect(reverse('group_detail_view', args=[group_code]))  # Redirect to the property list page
        else:
            print("this didn't work")
            messages.error(request, f"The user {user.first_name} {user.last_name} is not in the group: {group_code}")
            return redirect(reverse('group_detail_view', args=[group_code]))  # Redirect to the property list page
    else:
        return redirect(reverse('group_detail_view', args=[group_code]))


from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

@user_is_group_admin('secret_santa')
def create_assignment(request, group_code):
    user = request.user
    # Get the group instance by the group_code
    group = get_object_or_404(Group, code=group_code)

    # Ensure that the Secret Santa assignments have been created
    group.assign_secret_santa(group)

    try:
        # Fetch the assignment for the current user (giver)
        giver_assignment = Assignment.objects.get(group=group, giver=user)
        receiver = giver_assignment.receiver
        gift_preference = receiver.user_gift_preference.first()  # assuming each receiver has one gift preference

    except Assignment.DoesNotExist:
        raise Http404("You don't have a Secret Santa assignment.")

    # Context data for the template
    context = {
        'project_name': PROJECT_NAME,
        'project_year': PROJECT_YEAR,
        'group': group,
        'receiver': receiver,
        'gift_preference': gift_preference,
    }

    # # Check if the form was submitted (POST request)
    # if request.method == "POST":
    #     # Handle form submission (if any)
    #     pass

    return render(request, "secret_santa/assigned_secret_santa.html", context)

@user_belongs_to_group('secret_santa')
def assignment_view(request, group_code):
    user = request.user
    group = get_object_or_404(Group, code=group_code)
    assignment = Assignment.objects.get(group=group, giver=user)
    receiver = assignment.receiver
    gift_preference = GiftPreference.objects.filter(group=group, user=receiver).first()

    # print('gift_preference', gift_preference.gift.split())

    def parse_wishlist(wishlist: str):
        # Split the input into lines
        lines = wishlist.split('\n')
        
        # Clean up each line: strip leading/trailing spaces and filter out empty lines
        cleaned_gifts = [line.strip() for line in lines if line.strip()]
        
        return cleaned_gifts

    parsed_gifts = parse_wishlist(gift_preference.gift)

    context = {
        'group': group,
        'receiver': receiver,
        'gift_preference_gift': parsed_gifts,
    }

    return render(request, 'secret_santa/assigned_secret_santa.html', context)

# Websocket code
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings

def broadcast_json_data(group_code, json_data):
    # Get the channel layer
    channel_layer = get_channel_layer()

    # Broadcast the ticks to all WebSocket clients in the specified group
    async_to_sync(channel_layer.group_send)(
        group_code,  # Use group_code to target the correct group
        {
            "type": "new_ticks",  # This should match the consumer method
            "content": json.dumps(json_data),  # The data you want to send
        }
    )
