from django import forms
from django.contrib import admin
from .models import Task


class TaskChangeForm(forms.ModelForm):
	
	def clean_password(self):
		return self.initial['password']
	
	class Meta:
		model = Task
		fields = "__all__"
	
	def save(self, commit=True):
		task = super(TaskChangeForm, self).save(commit=False)
		task.save()
	
		teams_solved = list(task.teams_solved.all())
		for team in teams_solved:
			team.scores = sum([task.cost for task in team.tasks_solved.all()])
			team.save()
		return task


class TaskAdmin(admin.ModelAdmin):
	form = TaskChangeForm


admin.site.register(Task, TaskAdmin)
