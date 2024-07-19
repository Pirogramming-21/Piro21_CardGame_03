from django.shortcuts import render, redirect
from .models import Rank
from apps.users.models import User
from django.contrib.auth import get_user_model

# Create your views here.
def ranking(request):
    all_users = Rank.objects.order_by('-score')
    
    top_users = all_users[:3]
    
    ctx = {
        'top_users': top_users,
        'all_users': all_users
    }
    
    return render(request, 'rank/list.html', ctx)