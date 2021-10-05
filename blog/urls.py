from . import views
from django.urls import path

urlpatterns = [
    path('<int:pk>/',views.single_post_page),
    path('', views.index),     #서버IP/blog
]