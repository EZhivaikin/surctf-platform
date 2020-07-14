from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from teams.models import Team


def index(request):
    if request.user.is_authenticated:
        redirect('tasks_index')
    return redirect('login_url')

@login_required
def rating(request):
    classification = request.GET.get('class', default=None)
    classifications = [x[0] for x in Team.CLASSIFICATION]
    if classification is None:
        teams = Team.objects.filter(is_admin=False)
    elif classification in classifications:
        teams = Team.objects.filter(is_admin=False, classification=classification)
    else:
        return HttpResponse(status=404)
    return render(request, 'rating/rating.html', {'teams': teams.order_by('-scores','last_complete_date')})