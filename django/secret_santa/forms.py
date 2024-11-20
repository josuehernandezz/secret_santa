from django import forms
from .models import Group, GiftPreference

class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter group name'}),
        }

class GroupJoinForm(forms.Form):
    code = forms.CharField(max_length=8, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter group code'}))

class GiftPreferenceForm(forms.ModelForm):
    class Meta:
        model = GiftPreference
        fields = ['gift_list', 'max_price']
        widgets = {
            'gift_list': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your gift preferences (comma separated)'}),
            'max_price': forms.NumberInput(attrs={'placeholder': 'Enter maximum price'}),
        }
