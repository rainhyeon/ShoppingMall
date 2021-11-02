from . import views
from django.urls import path

urlpatterns = [ # 서버IP/blog/

    path('tag/<str:slug>', views.tag_page),
    path('category/<str:slug>', views.category_page),# 서버IP/blog/category/slug
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
]