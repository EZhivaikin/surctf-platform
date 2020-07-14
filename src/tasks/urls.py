from django.urls import path
from . import views


urlpatterns = [
	path('', views.index, name='tasks_index'),
	path('send_flag', views.send_flag, name='send_flag'),
	path('<int:task_id>/', views.get_task, name='get_task')
]