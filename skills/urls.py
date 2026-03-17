from django.urls import path
from . import views

urlpatterns = [
    path("skill/", views.skill_list, name="skill_list"),
    path("edit-skill/<int:id>", views.edit_skill, name="edit_skill"),
    path("delete-skill/<int:id>", views.delete_skill, name="delete_skill"),
    path("goal/", views.daily_goal, name="daily_goal"),
    path("edit-goal/<int:id>", views.edit_goal, name="edit_goal"),
    path("delete-goal/<int:id>", views.delete_goal, name="delete_goal"),
    path("toggle-goal/<int:id>", views.toggle_goal, name="toggle_goal"),
    path("", views.home_page, name="home_page"),
    path("notifications/", views.notifications, name="notifications"),
    # path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.user_login, name="user_login"),
    path("register/", views.user_register, name="user_register"),
    path("logout/", views.user_logout, name="user_logout"),
]
