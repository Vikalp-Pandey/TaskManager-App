from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .models import Task

# Create your views here.
class CustomLoginView(LoginView):
    template_name='App/login.html'
    fields="__all__"
    redirect_authenticated_user=True
    # *Creating a custom success_url 
    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name='App/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True
    # success_url=reverse_lazy('login')

    def form_valid(self,form):
        user=form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage,self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('login')
        return super(RegisterPage,self).get(*args, **kwargs)
    

class TaskList(LoginRequiredMixin,ListView):
    model=Task
    context_object_name="tasks"
    
    # *Showing the user specific data(tasks) only.
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count()
        return context
    
class TaskDetail(LoginRequiredMixin, DetailView): 
    model=Task
    context_object_name="task" 
    template_name="App/task_detail.html"
    
class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title','description','complete']
    success_url= reverse_lazy('tasks')
    # *Note: Django provides built ModelForms for all the models we created. 
    # *We can override the fields in modelForms by specifying fields attribute.


    def form_valid(self, form):
        form.instance.user=self.reuest.user
        return super(TaskCreate,self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','complete']
    success_url= reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')
