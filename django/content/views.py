from django.shortcuts import render
from home.settings import PROJECT_NAME, PROJECT_YEAR
# Create your views here.

def home(request):
    context = {
        'project_name': PROJECT_NAME,
        'project_year': PROJECT_YEAR,
    }
    return render(request, 'home.html', context)
