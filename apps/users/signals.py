from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount

@receiver(user_signed_up)
def populate_user_profile(request, user, **kwargs):
    print(f'Signal received for user: {user.username}')  # 디버깅 로그 추가
    if kwargs.get('sociallogin'):
        social_account = SocialAccount.objects.filter(user=user, provider='naver').first()
        if social_account:
            extra_data = social_account.extra_data
            print(f'Extra data from Naver: {extra_data}')  # 디버깅 로그 추가
            user.nickname = extra_data.get('nickname', 'User')  # 기본값 설정
            user.email = extra_data.get('email', '')
            user.username = extra_data.get('id', '')  # Naver의 고유 ID를 username으로 사용
            user.save()
            print(f'User profile updated: {user.nickname}, {user.email}, {user.username}')  # 디버깅 로그 추가
        else:
            print('No social account found for Naver.')  # 디버깅 로그 추가
    else:
        print('No sociallogin found in kwargs.')  # 디버깅 로그 추가