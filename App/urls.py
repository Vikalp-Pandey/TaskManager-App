from django.urls import path
from .views import RegisterPage, TaskCreate, TaskList,TaskDetail, TaskUpdate, TaskDelete,CustomLoginView,HomeView
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from App import views

urlpatterns=[
     path('', TemplateView.as_view(template_name='App/welcome.html'), name='welcome'), # This is the main change!
    #  path('welcome/', TemplateView.as_view(template_name='App/welcome.html'), name='welcome'), # This is the main change!
     path('tasks/',TaskList.as_view(), name='tasks'),
     path('login/', CustomLoginView.as_view(), name='login'),
     path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
     path('register/', RegisterPage.as_view(), name='register'),
     
     
     path('task/<int:pk>/',TaskDetail.as_view(), name='task'),
     path('task-create/',TaskCreate.as_view(),name='task-create'),
     path('task-upate/<int:pk>/',TaskUpdate.as_view(),name='task-update'),
     path('task-delete/<int:pk>/',TaskDelete.as_view(),name='task-delete'),
    path('task/<int:pk>/toggle/', views.task_toggle_complete, name='task-toggle-complete'),
]
