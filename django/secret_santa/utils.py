from .models import GiftPreference

def return_members_data(group, members):
    members_data = []

    for member in members:
        gift_preference_exists = GiftPreference.objects.filter(group=group, user=member).exists()
        members_data.append({
            'username': member.username,
            'first_name': member.first_name,
            'last_name': member.last_name,
            'gift_added': gift_preference_exists,
        })
    return members_data

# @login_required
# def get_updated_members(request, group_code):
#     # Get the group using the group_code
#     group = Group.objects.get(code=group_code)
    
#     # Get members and their gift preferences
#     members = group.members.all()
#     members_data = []
    
#     for member in members:
#         gift_preference_exists = GiftPreference.objects.filter(group=group, user=member).exists()
#         members_data.append({
#             'username': member.username,
#             'first_name': member.first_name,
#             'last_name': member.last_name,
#             'gift_added': gift_preference_exists,
#         })
    
#     return JsonResponse({'members': members_data})