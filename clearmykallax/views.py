from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from signups.forms import SendLinkForm


@require_GET
def landing(request):
    if request.user.is_authenticated:
        return redirect('games:list')

    context = {
        'emailform': SendLinkForm(),
    }
    return render(request, 'landing.html', context)


# from https://adamj.eu/tech/2022/01/18/how-to-add-a-favicon-to-your-django-site/
@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = (settings.BASE_DIR / "clearmykallax" / "static" / "favicon.png").open("rb")
    return FileResponse(file)


# from https://adamj.eu/tech/2020/02/10/robots-txt/#with-a-custom-view
@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
