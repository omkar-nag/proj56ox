
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API Route
    path("posts/<str:param>",views.allposts, name="posts"),
    path("create",views.newpost, name="create"),
    path("profile/<str:user1>",views.profile,name="profile"),
    path("follow/<str:target>",views.follow,name="follow"),
    path("like/<int:postid>",views.like,name='like')
]
