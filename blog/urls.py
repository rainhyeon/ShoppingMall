from . import views
from django.urls import path

urlpatterns = [

    path('category/<str:slug>', views.category_page),
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
]