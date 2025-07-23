from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView

from .models import Task

# Create your views here.

class TaskList(ListView):
    model=Task
    context_object_name="tasks"

class TaskDetail(DetailView): 
    model=Task
    context_object_name="task" 
    template_name="App/task_detail.html"
    
class TaskCreate(CreateView):
    model=Task
    fields="__all__"
    # fields=['title','description']
    success_url= reverse_lazy('tasks')
    # ? Note: Django provides built ModelForms for all the models we created. 
    # ?We can override the fields in modelForms by specifying fields attribute.

class TaskUpdate(UpdateView):
    model=Task
    fields="__all__"
    success_url= reverse_lazy('tasks')

class TaskDelete(DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')
