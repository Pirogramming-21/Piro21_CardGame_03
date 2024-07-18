from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import get_user_model

User = get_user_model()

def main(request):
    return render(request, "users/main.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        nickname = request.POST['nickname']
        birth = request.POST['birth']
        gender = request.POST['gender']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            context = {'error': '이미 존재하는 Username입니다.'}
            return render(request, 'users/signup.html', context=context)

        user = User.objects.create_user(
            username=username, 
            password=password, 
            nickname=nickname, 
            birth=birth, 
            gender=gender, 
            email=email
        )
        auth.login(request, user)
        return redirect("users:main")

    return render(request, 'users/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('users:main')
        else:
            context = {'error': '적절하지 않은 Username이나, Password입니다. 다시 입력해주세요.'}
            return render(request, 'users/login.html', context=context)

    return render(request, 'users/login.html')

def logout(request):
    auth.logout(request)
    return redirect('users:main')
