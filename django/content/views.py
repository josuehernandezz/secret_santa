from django.shortcuts import render
from home.settings import PROJECT_NAME
# Create your views here.

def home(request):
    context = {
        'project_name': PROJECT_NAME,
    }
    return render(request, 'home.html', context)
