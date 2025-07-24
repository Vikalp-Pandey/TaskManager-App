from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task

# Create your views here.
class CustomLoginView(LoginView):
    template_name='App/login.html'
    fields="__all__"
    redirect_authenticated_user=True
   
    # *Creating a custom success_url 
    def get_success_url(self):
        return reverse_lazy('tasks')


class TaskList(LoginRequiredMixin,ListView):
    model=Task
    context_object_name="tasks"

class TaskDetail(DetailView): 
    model=Task
    context_object_name="task" 
    template_name="App/task_detail.html"
    
class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields="__all__"
    # fields=['title','description']
    success_url= reverse_lazy('tasks')
    # *Note: Django provides built ModelForms for all the models we created. 
    # *We can override the fields in modelForms by specifying fields attribute.

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields="__all__"
    success_url= reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')
