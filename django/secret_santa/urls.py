from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('secret_santa', views.secret_santa, name='secret_santa'),
    path('group_view', views.group_view, name='group_view'),
]
