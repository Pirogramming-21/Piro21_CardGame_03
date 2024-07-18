from django.shortcuts import render, redirect
from .models import Rank
from apps.users.models import User
from django.contrib.auth import get_user_model

# Create your views here.
def list(request):
    users = User.objects.order_by('-score')[3]
    return render(request, 'rank_list.html', {'users': users})