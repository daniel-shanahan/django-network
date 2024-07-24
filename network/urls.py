from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("users/<int:id>", views.profile, name="profile"),
    path("users/<int:id>/follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("post/<int:post_id>", views.post, name="post"),
]
