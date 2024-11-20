import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Helper function to generate a random code
def generate_group_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class Group(models.Model):
    code = models.CharField(max_length=8, blank=True, null=False, unique=True)
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='secret_santa_groups')
    created_at = models.DateTimeField(default=timezone.now)

    def add_user(self, user):
        # Add a user to the group's members using ManyToManyField's add method
        self.members.add(user)

    def save(self, *args, **kwargs):
        if not self.code:  # Generate group code if it doesn't exist
            self.code = generate_group_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} | {self.code}"

class GiftPreference(models.Model):
    user = models.ForeignKey(User, related_name='user_gift_preference', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='gift_preferences', on_delete=models.PROTECT)  # Custom related_name
    gift_list = models.TextField()  # List of preferred gifts (can be JSON or a string)
    max_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s preferences in {self.group.name} | {self.group.code}"

class Assignment(models.Model):
    giver = models.ForeignKey(User, related_name='giver', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='assignments', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.giver.username} -> {self.receiver.username} in {self.group.name}"
