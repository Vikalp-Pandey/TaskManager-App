from django.utils import timezone

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

from App.forms import CustomUserCreationForm
from .models import Task,UserProfile
from .forms import CustomUserCreationForm
import pytz
from django.shortcuts import get_object_or_404, redirect
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
    form_class=CustomUserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('login')

    def form_valid(self,form):
        user=form.save()
        if user is not None:
            # *Log the user in immediately after registration
            login(self.request, user)
        return super(RegisterPage,self).form_valid(form)

    # def get(self, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         return redirect('login')
    #     return super(RegisterPage,self).get(*args, **kwargs)
    

class TaskList(LoginRequiredMixin,ListView):
    model=Task
    context_object_name="tasks"
    
    
    def get_queryset(self):
        # Base queryset filtered by user
        queryset = Task.objects.filter(user=self.request.user)

        # Apply search filter
        search_input = self.request.GET.get('search-area', '')
        if search_input:
            queryset = queryset.filter(title__icontains=search_input)

        # Apply sorting
        sort = self.request.GET.get('sort', '')
        if sort == 'created_at_desc':
            queryset = queryset.order_by('-created_at')
        elif sort == 'created_at_asc':
            queryset = queryset.order_by('created_at')
        elif sort == 'title':
            queryset = queryset.order_by('title')

        return queryset
    
    # *Showing the user specific data(tasks) only.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        # Applying Search Filter
        search_input = self.request.GET.get('search-area', '')  # Use empty string as default
        if search_input:  # Only apply filter if search_input is non-empty
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input

        # Use user profile timezone if available, else fallback to UTC
        user_timezone = 'UTC'
        if self.request.user.is_authenticated:
            try:
                user_timezone = self.request.user.profile.timezone
            except UserProfile.DoesNotExist:
                pass
        print(f"User timezone applied: {user_timezone}")
        try:
            timezone.activate(pytz.timezone(user_timezone))
            context['user_timezone'] = user_timezone
        except pytz.exceptions.UnknownTimeZoneError:
            timezone.activate(pytz.timezone('UTC'))
            context['user_timezone'] = 'UTC'
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
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','complete']
    success_url= reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')


from django.shortcuts import get_object_or_404, redirect
from .models import Task

def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == 'POST':
        task.complete = not task.complete
        task.save()
    return redirect('tasks')

class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # If user is logged in, redirect to their task list
            return redirect('tasks')
        else:
            # If user is not logged in, show the welcome page
            return render(request, 'App/welcome.html')
