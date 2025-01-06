
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_post, name="create"),
    path("user/<int:id>/", views.user_profile, name="user_profile"),
    path("is_following/<int:id>", views.is_following, name="is_following"),
    path("user/<int:id>/followings", views.following, name="following"),
    path("user/<int:id>/followers", views.followers, name="followers"),
    path("edit_post/", views.edit_post, name="edit_post"),
    path("like_post/<int:post_id>", views.like_post, name="like_post"),
]
