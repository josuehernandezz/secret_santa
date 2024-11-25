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
    description = models.TextField(max_length=5000, blank=True, null=True)
    rules = models.TextField(max_length=5000, blank=True, null=True)
    admin = models.ForeignKey(User, related_name='admin_secret_santa_group', on_delete=models.CASCADE, blank=False, null=True)
    members = models.ManyToManyField(User, related_name='secret_santa_groups')
    created_at = models.DateTimeField(default=timezone.now)

    def add_admin(self, user):
        self.admin = user

    def add_user(self, user):
        # Add a user to the group's members using ManyToManyField's add method
        self.members.add(user)

    def save(self, *args, **kwargs):
        if not self.code:  # Generate group code if it doesn't exist
            self.code = generate_group_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.admin.username} | {self.name} | {self.code}"

    @property
    def all_users_assigned_secret_santa(self):
        # Retrieve all users in the group
        members = self.members.all()

        # Check if each member has an assignment
        for member in members:
            # Check if there's an assignment for this member (giver or receiver)
            if not Assignment.objects.filter(group=self, giver=member).exists():
                return False  # If any member doesn't have an assignment, return False

        return True  # If all members have assignments, return True

    @property
    def all_members_have_gift(self):
        # Retrieve all users in the group
        members = self.members.all()

        # Check if each member has a gift preference
        for member in members:
            if not member.user_gift_preference.exists():  # If no gift preference exists
                return False  # If one member doesn't have a gift preference, return False

        return True  # If all members have a gift preference, return True

    @classmethod
    def assign_secret_santa(cls, group):
        """
        Assign a random 'Secret Santa' to each user in the group.
        Each user will be assigned to buy a gift for another member (not themselves).
        """
        members = list(group.members.all())  # Get all members as a list

        if len(members) < 2:
            print("Not enough members to assign Secret Santa.")
            return None

        # Shuffle the list of members
        random.shuffle(members)

        # Initialize a dictionary to hold the assignments
        assignments = {}

        # Ensure no one is assigned to themselves
        for i in range(len(members)):
            # The current person in the list will give a gift to the next person
            # If it's the last person, they will give a gift to the first person (circular assignment)
            giver = members[i]
            receiver = members[(i + 1) % len(members)]  # Next person, circular at the end

            assignments[giver] = receiver

        # You can store these assignments in a new model or update an existing field on the User model.
        # Here is an example of how to store them in a model (assuming you have a model to track Secret Santa assignments):

        # Clear any existing assignments before saving new ones
        Assignment.objects.filter(group=group).delete()

        # Save the new assignments
        for giver, receiver in assignments.items():
            Assignment.objects.create(group=group, giver=giver, receiver=receiver)

        return assignments

class GiftPreference(models.Model):
    user = models.ForeignKey(User, related_name='user_gift_preference', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='gift_preferences', on_delete=models.CASCADE)  # Custom related_name
    gift = models.TextField(max_length=10000, blank=False, null=True)

    def __str__(self):
        return f"{self.user.username.capitalize()}'s gift list in {self.group.name} | {self.group.code}"

class Assignment(models.Model):
    giver = models.ForeignKey(User, related_name='giver', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='assignments', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.giver.username} -> {self.receiver.username} in {self.group.name}"
