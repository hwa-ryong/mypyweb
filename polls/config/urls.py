from django.contrib import admin
from django.urls import path, include
from poll import views

from poll import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('poll/', include('poll.urls')),
    path('', views.index),   #http://127.0.0.1:8000/
]
