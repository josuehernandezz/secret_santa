from django import forms
from .models import Group, GiftPreference

style = 'bg-zinc-50 border border-zinc-300 text-zinc-900 text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2.5  dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white dark:focus:ring-green-500 dark:focus:border-green-500'

class GroupCreationForm(forms.ModelForm):
    name = forms.CharField(label='Group Name', max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Office Secret Santa, December 2024',
        'autofocus': False,
        'class': style,
        }))
    description = forms.CharField(
        label='Group Description',
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': "Welcome to the office gift exchange! This is the group for our team’s annual Secret Santa event.",
            'autofocus': False,
            'class': style,
            'rows': 3,
            'cols': 50
        }))
    rules = forms.CharField(
        label='Group Rules',
        required=True,
        initial='''Example rules:
1. Set a budget limit for gifts to keep things fair. (e.g., $20-$30)
2. Provide a wish list of at least 3-5 gift ideas to help your Secret Santa pick something you'll enjoy.
3. Keep your identity a secret until the gift is opened.
4. All gifts must be given on the set date. (e.g. December 24th)
5. Please wrap your gift or present it in a way that hides who it’s from.
6. Be grateful of the gift(s) that you receive!''',
        widget=forms.Textarea(attrs={
            'placeholder': '''Example rules:
1. Set a budget limit for gifts to keep things fair. (e.g., $20-$30)
2. Provide a wish list of at least 3-5 gift ideas to help your Secret Santa pick something you'll enjoy.
3. Keep your identity a secret until the gift is opened.
4. All gifts must be given on the set date. (e.g. December 24th)
5. Please wrap your gift or present it in a way that hides who it’s from.
6. Be grateful of the gift(s) that you receive!''',
            'autofocus': False,
            'class': style,
            'rows': 9,
            'cols': 50
        }))
    class Meta:
        model = Group
        fields = ['name', 'description', 'rules']

class GroupJoinForm(forms.Form):
    code = forms.CharField(label='Group Code', 
        max_length=8, 
        required=True, 
        widget=forms.TextInput(attrs={
        'placeholder': "Enter your family or friend's 8 character group code.",
        'autofocus': False,
        'class': style,
        }))
    # code = forms.CharField(max_length=8, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter group code'}))

class GiftPreferenceForm(forms.ModelForm):
    class Meta:
        model = GiftPreference
        fields = ['gift']

    gift = forms.CharField(
        label='Gift Description',
        # max_length=2000,
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 
'''Example message for your secret santa:
1. A cozy, soft blanket or throw
2. A fun puzzle or board game for a relaxing evening
3. A scented candle or essential oils set to create a calming atmosphere
4. A nice mug with a cute design (I love coffee!)
5. A quirky plant or succulent to brighten up my desk or home
6. A LEGO set (I love building and it's a fun way to relax!)
            ''',
            'autofocus': False,
            'class': style,
            'rows': 8,
            'cols': 50
        }))

# class DeleteUserFromGroupForm(forms.Form):
#     delete_user = forms.BooleanField(
#         label='Delete User',
#         required=False,  # Optional field
#         widget=forms.CheckboxInput(attrs={
#             'class': 'w-4 h-4 text-red-600 bg-zinc-100 border-zinc-300 rounded focus:ring-red-500 dark:focus:ring-red-600 dark:ring-offset-zinc-800 focus:ring-2 dark:bg-zinc-700 dark:border-zinc-600',  # Custom class for styling
#             'id': 'delete-user-checkbox',  # Optional ID for targeting in JS or CSS
#             'data-toggle': 'tooltip',  # Example of adding custom data attributes
#         })
#     )

class DeleteUserFromGroupForm(forms.Form):
    # This form will dynamically generate checkboxes for each group member
    delete_user = forms.BooleanField(
        label='Delete User',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-red-600 bg-zinc-100 border-zinc-300 rounded focus:ring-red-500 dark:focus:ring-red-600 dark:ring-offset-zinc-800 focus:ring-2 dark:bg-zinc-700 dark:border-zinc-600',
        })
    )

    # def __init__(self, *args, **kwargs):
    #     group_members = kwargs.pop('group_members', [])
    #     super().__init__(*args, **kwargs)

    #     # Dynamically add a checkbox for each group member
    #     for member in group_members:
    #         self.fields[f'delete_user_{member.id}'] = forms.BooleanField(
    #             label=f"Delete {member.first_name} {member.last_name}",
    #             required=False,
    #             widget=forms.CheckboxInput(attrs={'class': 'delete-checkbox'}),
    #         )
