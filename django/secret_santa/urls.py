from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('secret_santa', views.secret_santa, name='secret_santa'),
    # path('group_list_view', views.group_list_view, name='group_list_view'),
    path('groups', views.group_list_view, name='group_list_view'),
    # path('group_detail_view/<str:group_code>', views.group_detail_view, name='group_detail_view'),
    path('group/<str:group_code>', views.group_detail_view, name='group_detail_view'),
    path('remove_user_from_group/<str:group_code>/<int:user_id>', views.remove_user_from_group, name='remove_user_from_group'),
    path('create_assignment/<str:group_code>', views.create_assignment, name='create_assignment'),
    path('assignment/<str:group_code>', views.assignment_view, name='assignment_view')
]
