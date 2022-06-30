from django.urls import path

from . import views

app_name='todo'

urlpatterns=[
	path('', views.home, name='home'),
	path('login/', views.login, name='login'),
	path('register/', views.register, name='register'),
	path('logout/', views.logout, name='logout'),
	path('delete_todo/<int:pk>', views.delete_todo, name='delete_todo'),
	path('update_todo/<int:pk>', views.update_todo, name='update_todo'),
]