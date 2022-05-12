from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from games.forms import FilterForm
from games.models import Game


@login_required
def games_list(request):
    filterform = FilterForm.from_request(request)

    queryset = Game.objects.all()
    if filterform.is_bound:
        queryset = filterform.apply_to_queryset(queryset)

    return render(request, 'games/list.html', {
        'games': queryset,
        'filterform': filterform,
    })


@login_required
def detail(request, slug):
    game = get_object_or_404(Game, slug=slug)
    return render(request, 'games/detail.html', {'game': game})
