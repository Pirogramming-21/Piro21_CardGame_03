from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import GameForm
from .models import Game
from apps.rank.models import Rank
import random

@login_required
def attack(request):
    random_numbers = random.sample(range(1, 11), 5)
    if request.method == 'POST':
        player1_card = request.POST.get('player1_card')
        form = GameForm(request.POST, request=request, random_numbers=random_numbers)
        if form.is_valid():
            opponent = form.cleaned_data['opponent']
            win_condition = random.choice(['HIGHER', 'LOWER'])
            game = Game.objects.create(player1=request.user, player2=opponent, player1_card=player1_card, win_condition=win_condition)
            return redirect('games:list')
    else:
        form = GameForm(request=request, random_numbers=random_numbers)
    return render(request, 'games/attack.html', {'form': form, 'random_numbers': random_numbers})

@login_required
def game_list(request):
    user = request.user
    games_as_player1 = Game.objects.filter(player1=user).order_by('-created_at')
    games_as_player2 = Game.objects.filter(player2=user).order_by('-created_at')
    return render(request, 'games/list.html', {
        'games_as_player1': games_as_player1,
        'games_as_player2': games_as_player2,
    })

@login_required
def counter_attack(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        player2_card = request.POST.get('player2_card')
        if player2_card is not None:
            game.player2_card = int(player2_card)
            game.status = 'COMPLETED'

            try:
                player2_card = int(player2_card)
            except ValueError:
                return redirect('games:list')
            
            game.player2_card = player2_card
            game.status = 'COMPLETED'

            player1_card = game.player1_card
            
            if game.win_condition == 'HIGHER':
                if game.player1_card > game.player2_card:
                    game.result = 'WIN'
                    update_score(game.player1, player1_card)
                    update_score(game.player2, -player1_card)
                elif game.player1_card < game.player2_card:
                    game.result = 'LOSE'
                    update_score(game.player1, -player2_card)
                    update_score(game.player2, player2_card)
                else:
                    game.result = 'DRAW'
            else:  # LOWER
                if game.player1_card < game.player2_card:
                    game.result = 'WIN'
                    update_score(game.player1, player1_card)
                    update_score(game.player2, -player2_card)
                elif game.player1_card > game.player2_card:
                    game.result = 'LOSE'
                    update_score(game.player1, -player1_card)
                    update_score(game.player2, player2_card)
                else:
                    game.result = 'DRAW'
            
            game.save()
            return redirect('games:list')
        else:
            return redirect('games:counter_attack', pk=pk)

    random_numbers = random.sample(range(1, 11), 5)
    return render(request, 'games/counter_attack.html', {'game': game, 'random_numbers': random_numbers})

@login_required
def game_cancel(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if game.status == 'PENDING' and game.player1 == request.user:
        game.delete()
    return redirect('games:list')

@login_required
def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    game_index = Game.objects.filter(created_at__lt=game.created_at).count() + 1  # 게임의 순서 계산
    return render(request, 'games/detail.html', {'game': game, 'game_index': game_index})

def update_score(user, points):
    rank, created = Rank.objects.get_or_create(user=user)
    rank.score += points
    rank.save()
