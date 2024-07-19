from django.shortcuts import render, redirect
from .models import Rank
from apps.users.models import User
from django.contrib.auth import get_user_model

# Create your views here.
def ranking(request):
    users = Rank.objects.order_by('-score')
    if len(users) > 3:
        users = users[:3]  
    else:
        users = users  
    ctx = {'users':users}
    return render(request, 'rank/list.html', ctx)