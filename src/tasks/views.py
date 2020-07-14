from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from tasks.models import Task
from teams.models import Team


@login_required
def index(request):
    team: Team = request.user
    tasks_solved = list(team.tasks_solved.all())
    tasks = list(Task.objects.all().order_by('category'))
    for task in tasks:
        task.solved = True if task in tasks_solved else False
    return render(request, 'tasks.html', {'tasks': tasks})


@login_required
def send_flag(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        team: Team = request.user

        if not task_id:
            HttpResponse(status=400)
            
        flag = request.POST.get('flag')
        if not flag:
            HttpResponse(status=400)

        task = Task.objects.get(id=task_id)
        
        if task.flag == flag or task in team.tasks_solved.all():
            team.tasks_solved.add(task)
            team.scores = sum([x.cost for x in team.tasks_solved.all()])
            team.last_complete_date = timezone.now()
            team.save()
            return render(request, 'task.html', {'task': task, 'solved': True})
        return render(request, 'task.html', {'task': task, 'solved': False})
    else:
        return HttpResponse(status=405)
    
@login_required
def get_task(request, task_id):
    if task_id is None:
        HttpResponse(status=404)
        
    task = Task.objects.get(id=task_id)
    if task is None:
        HttpResponse(status=404)
    team: Team = request.user
    task.solved = True if task in team.tasks_solved.all() else None
    return render(request,'task.html',{'task':task, 'solved': task.solved})