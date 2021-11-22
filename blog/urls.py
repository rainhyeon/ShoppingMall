from . import views
from django.urls import path

urlpatterns = [ # 서버IP/blog/

    path('search/<str:q>/', views.PostSearch.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('tag/<str:slug>', views.tag_page),
    path('category/<str:slug>', views.category_page),# 서버IP/blog/category/slug
    path('<int:pk>/new_comment/', views.new_comment),
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
]