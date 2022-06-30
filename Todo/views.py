from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from .models import Todo

# Create your views here.

def home(request):

	#create a task
	if request.method == 'POST':
		todo_name = request.POST.get('task')
		if todo_name:
			Todo.objects.create(name=todo_name, user=request.user)
		return HttpResponseRedirect(reverse('todo:home'))

	# redirect anonymous user to login page otherwise to the home page where there are tasks's user
	if request.user.is_authenticated:
		user_tasks = Todo.objects.filter(user=request.user)
		return render(request, 'todo/home.html', {'user_tasks':user_tasks})
	return HttpResponseRedirect(reverse('todo:login'))

def login(request):

	# we check if the user is logged in and he accessed the login page 
	# then we redirect him to the home page
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('todo:home'))
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)

		if not username and not password:
			return render(request, 'todo/login.html', {'error':'Check your information please and fill all the blanks'})

		if user is not None:
			auth_login(request, user)
			return HttpResponseRedirect(reverse('todo:home'))

		return render(request, 'todo/login.html', {'error':'User is not exist, check your information or create a new account'})

	return render(request, 'todo/login.html')

def register(request):

	# the same thing for register page
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('todo:home'))
	if request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		# we check that the user fill all the blanks otherwise we will throw him an error
		if username and email and password:
			user = User.objects.create_user(username, email, password)
			user.save()
			return HttpResponseRedirect(reverse('todo:login'))
		return render(request, 'todo/register.html', {'error':'Check your information please and fill all the blanks'})


	return render(request, 'todo/register.html')

def logout(request):

	auth_logout(request)
	return HttpResponseRedirect(reverse('todo:login'))

def delete_todo(request, pk):
	# get the todo object for the specific user
	todo = get_object_or_404(Todo, id=pk, user=request.user)
	todo.delete()

	return HttpResponseRedirect(reverse('todo:home'))

def update_todo(request, pk):

	if request.method == 'POST':
		todo = get_object_or_404(Todo, id=pk, user=request.user)
		todo_name = request.POST.get(f"task{pk}")
		todo.name = todo_name
		todo.save()
		return HttpResponseRedirect(reverse('todo:home'))
	return render(request, 'todo/update.html', {'todo_id':pk})