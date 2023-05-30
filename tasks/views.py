from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):

    if request.method == 'GET':
        print('enviando formulario')

        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        print('obteniendo datos')
        print(request.POST)

        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
                #return HttpResponse('Usuario creado satisfactoriamente')
            except:
                return HttpResponse('El usuario ya existe')
        return HttpResponse('Las contraseñas no coinciden')

@login_required
def tasks(request):
    #tasks = Task.objects.all()
    #tasks = Task.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    #tasks = Task.objects.all()
    #tasks = Task.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        print(request.POST)

        form = TaskForm(request.POST)
        print(form)

        new_task = form.save(commit=False)
        new_task.user = request.user
        new_task.save()

        return redirect('tasks')

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        #task = Task.objects.get(pk=task_id)
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        print(request.POST)

        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(request.POST, instance=task)
        form.save()
        return redirect('tasks')

@login_required
def complete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.dateCompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.delete()
        return redirect('tasks')

@login_required
def signout(request): #logout palabra reservada
    logout(request)
    return redirect('home')

def signin(request): #login palabra reservada
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        print(request.POST)

        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o password incorrectos'
            })
        else:
            login(request, user)
            return redirect('tasks')
    
