
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:username>",views.profile_view,name="profile"),
    path("apis/follow_unfollow/<str:username>",views.follow_unfollow,name="follow_unfollow"),
    path("following",views.following,name="following"),
    path("apis/like_unlike/<int:id>",views.like_unlike,name="like_unlike"),
    path("edit_post/<int:id>",views.edit,name="edit_post")
    # path("<int:id>",views.profile_view,name="profile")
    # path("new", views.create_post, name="new")
]
