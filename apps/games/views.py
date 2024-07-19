from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import GameForm
from .models import Game
import random

@login_required
def attack(request):
    random_numbers = random.sample(range(1, 11), 5)
    if request.method == 'POST':
        player1_card = request.POST.get('player1_card')
        form = GameForm(request.POST, request=request, random_numbers=random_numbers)
        if form.is_valid():
            opponent = form.cleaned_data['opponent']
            win_condition = random.choice(['HIGHER', 'LOWER'])  # 승리 조건 설정
            game = Game.objects.create(player1=request.user, player2=opponent, player1_card=player1_card, win_condition=win_condition)
            return redirect('games:list')  # Redirect to the game list view
    else:
        form = GameForm(request=request, random_numbers=random_numbers)
    return render(request, 'games/attack.html', {'form': form, 'random_numbers': random_numbers})

@login_required
def game_list(request):
    user = request.user
    games_as_player1 = Game.objects.filter(player1=user).order_by('-created_at')  # 최신 게임이 위에 오도록 정렬
    games_as_player2 = Game.objects.filter(player2=user).order_by('-created_at')  # 최신 게임이 위에 오도록 정렬
    return render(request, 'games/list.html', {
        'games_as_player1': games_as_player1,
        'games_as_player2': games_as_player2,
    })

@login_required
def counter_attack(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        player2_card = request.POST.get('player2_card')
        game.player2_card = player2_card
        game.status = 'COMPLETED'

        # Determine the result based on win_condition
        if game.win_condition == 'HIGHER':
            if game.player1_card > game.player2_card:
                game.result = 'WIN'
            elif game.player1_card < game.player2_card:
                game.result = 'LOSE'
            else:
                game.result = 'DRAW'
        else:  # LOWER
            if game.player1_card < game.player2_card:
                game.result = 'WIN'
            elif game.player1_card > game.player2_card:
                game.result = 'LOSE'
            else:
                game.result = 'DRAW'

        game.save()
        return redirect('games:list')
    
    # Generate random choices for player2
    random_numbers = random.sample(range(1, 11), 5)
    return render(request, 'games/counter_attack.html', {'game': game, 'random_numbers': random_numbers})

@login_required
def game_cancel(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if game.status == 'PENDING' and game.player1 == request.user:  # 공격자가 자신인 경우에만 취소 가능
        game.delete()
    return redirect('games:list')