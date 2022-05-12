from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from games.forms import FilterForm
from games.models import Game


@login_required
def games_list(request):
    filterform = FilterForm.from_request(request)

    queryset = Game.objects.visible_to(request.user)
    if filterform.is_bound:
        queryset = filterform.apply_to_queryset(queryset)

    return render(request, 'games/list.html', {
        'games': queryset,
        'filterform': filterform,
    })


@login_required
def detail(request, slug):
    game = get_object_or_404(Game, slug=slug)
    if not game.is_visible:
        messages.error(request, "Sorry, this game is not available anymore")
    return render(request, 'games/detail.html', {'game': game})


@require_POST
@staff_member_required
def show_game(request, slug):
    game = get_object_or_404(Game, slug=slug)
    game.set_visibility(Game.VISIBILITY.VISIBLE)
    messages.success(request, f"The game \"{game.title}\" is now listed publicly")
    if success_url := request.POST.get('next'):
        return redirect(success_url)
    else:
        return redirect('game:detail', slug=slug)


@require_POST
@staff_member_required
def hide_game(request, slug):
    game = get_object_or_404(Game, slug=slug)
    game.set_visibility(Game.VISIBILITY.HIDDEN)
    messages.success(request, f"The game \"{game.title}\" is now hidden from the public site")
    if success_url := request.POST.get('next'):
        return redirect(success_url)
    else:
        return redirect('game:detail', slug=slug)
