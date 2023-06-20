from django.urls import path
from board import views

app_name = 'board'

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('question/create/', views.question_create,
         name='question_create'),
    path('answer/create/<int:question_id>/', views.answer_create,
         name='answer_create'),
]