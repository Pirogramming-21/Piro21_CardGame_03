from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount

User = get_user_model()

def main(request):
    context = {}
    if request.user.is_authenticated:
        context['user'] = request.user
        print(f"Logged in user: {request.user.username}, Nickname: {request.user.nickname}")  # 디버깅용
    return render(request, "users/main.html", context)

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
        
        # backend를 명시적으로 지정
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect("users:main")

    return render(request, 'users/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                context = {'error': 'Superuser는 로그인할 수 없습니다.'}
                return render(request, 'users/login.html', context=context)
            else:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('users:main')
        else:
            context = {'error': '적절하지 않은 Username이나, Password입니다. 다시 입력해주세요.'}
            return render(request, 'users/login.html', context=context)

    if request.user.is_authenticated:
        social_account = SocialAccount.objects.filter(user=request.user, provider='naver').first()
        if social_account:
            extra_data = social_account.extra_data
            print(f'Extra data from Naver in login view: {extra_data}')  # 디버깅 로그 추가
            request.user.username = extra_data.get('id', '')
            request.user.nickname = extra_data.get('nickname', 'User')  # 기본값 설정
            request.user.email = extra_data.get('email', '')
            request.user.save()
            print(f'User info updated in login view: {request.user.nickname}, {request.user.email}, {request.user.username}')  # 디버깅 로그 추가
        else:
            print('No social account found for Naver in login view.')  # 디버깅 로그 추가
        
    return render(request, 'users/login.html')

def logout(request):
    auth.logout(request)
    return redirect('users:main')

@login_required
def game_view(request):
    user = request.user
    context = {
        'nickname': user.nickname,
        'game_score': user.game_score,
        'level': user.level,
    }
    return render(request, 'users/main.html', context)

@login_required
def user_profile(request):
    user = request.user
    context = {
        'user': user,
        'social_account': user.socialaccount_set.first()
    }
    return render(request, 'users/profile.html', context)