from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),  #목록
    path('<int:post_id>/', views.detail, name='detail'),
    path('post/create/', views.post_create, name='post_create'),
]