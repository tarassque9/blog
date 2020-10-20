from django.urls import path
from .views import HomeView, LoginView, LogoutView, PostCreate, UserDetail, PostDetail, redirect_blog

urlpatterns = [
    path('', redirect_blog),
    path('home', HomeView.as_view(), name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('post_create', PostCreate.as_view(), name='post_create'),
    path('user_detail/<int:id>', UserDetail.as_view(), name='user_detail'),
    path('post_detail/<int:id>', PostDetail.as_view(), name='post_detail'),
    path('follow', PostDetail.as_view(), name='follow')
]
