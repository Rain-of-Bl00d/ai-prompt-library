from django.urls import path
from . import views

urlpatterns = [
    path('prompts/', views.prompt_list_create, name='prompt-list-create'),
    path('prompts/<int:pk>/', views.prompt_detail, name='prompt-detail'),
]