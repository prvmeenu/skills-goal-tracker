from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .models import Skill, Goal, User, Notification
from django.contrib.auth.decorators import login_required
from datetime import date, time, timedelta
import json


# Create your views here.
@login_required
def skill_list(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        level = request.POST.get("level")

        user_skills = Skill.objects.filter(user=request.user)

        if not name or len(name) < 3:
            error_message = {
                "error": "Skill name cannot be empty and cannot be less than 3 letters",
                "skills": Skill.objects.all(),
            }
            return render(request, "skills/skill_list.html", error_message)

        if not level or not level.isdigit():
            error_message = {
                "error": "Level cannot be empty and must have only numbers",
                "skills": Skill.objects.all(),
            }
            return render(request, "skills/skill_list.html", error_message)

        level_int = int(level)

        if level_int < 1 or level_int > 10:
            error_message = {
                "error": "Skill levels must be between 1 to 10",
                "skills": Skill.objects.all(),
            }
            return render(request, "skills/skill_list.html", error_message)

        if name and level:
            Skill.objects.create(name=name, level=level, user=request.user)
            return redirect("skill_list")

    skills = Skill.objects.filter(user=request.user)
    unread = Notification.objects.filter(user=request.user, status=False).count()
    recent_notification = Notification.objects.filter(user=request.user).order_by(
        "-created_at"
    )[:5]
    for skill in skills:
        skill.range = range(skill.level)
    return render(
        request,
        "skills/skill_list.html",
        {
            "skills": skills,
            "unread": unread,
            "recent_notification": recent_notification,
        },
    )


@login_required
def edit_skill(request, id):
    skill = get_object_or_404(Skill, id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        level = request.POST.get("level")

        skill.name = name
        skill.level = level
        skill.save()

        return redirect("skill_list")
    return render(request, "skills/edit_skill.html", {"skill": skill})


@login_required
def delete_skill(request, id):
    skill = get_object_or_404(Skill, id=id)
    skill.delete()
    return redirect("skill_list")


@login_required
def daily_goal(request):
    if request.method == "POST":
        goal = request.POST.get("goal", "").strip()
        status = request.POST.get("is_completed") == "on"

        if not goal or len(goal) < 3:
            error_message = {
                "error": "Goal cannot be empty and cannot be less than 3 letters",
                "goals": Goal.objects.all(),
            }
            return render(request, "skills/daily_goal.html", error_message)

        Goal.objects.create(goal=goal, is_completed=status, user=request.user)
        return redirect("daily_goal")

    filter_type = request.GET.get("filter", "all").lower()

    if filter_type == "completed":
        goals = Goal.objects.filter(user=request.user, is_completed=True)
    elif filter_type == "pending":
        goals = Goal.objects.filter(user=request.user, is_completed=False)

    else:
        goals = Goal.objects.filter(user=request.user)

    # goals_count = goals.count()
    # goals = Goal.objects.all()
    total_goal = goals.count()

    completed_goal = goals.filter(is_completed=True).count()
    pending_goal = goals.filter(is_completed=False).count()

    if total_goal > 0:
        progress = int((completed_goal / total_goal) * 100)
    else:
        progress = 0

    unread = Notification.objects.filter(user=request.user, status=False).count()
    recent_notification = Notification.objects.filter(user=request.user).order_by(
        "-created_at"
    )[:5]

    context = {
        "goals": goals,
        "total": total_goal,
        "completed": completed_goal,
        "pending": pending_goal,
        "progress_bar": progress,
        "unread": unread,
        "recent_notification": recent_notification,
    }

    return render(request, "skills/daily_goal.html", context)


@login_required
def edit_goal(request, id):
    goal = get_object_or_404(Goal, id=id)

    if request.method == "POST":
        goal_value = request.POST.get("goal")
        is_completed = request.POST.get("is_completed") == "on"

        goal.goal = goal_value
        goal.is_completed = is_completed
        goal.save()

        return redirect("daily_goal")
    return render(request, "skills/edit_goal.html", {"goal": goal})


@login_required
def toggle_goal(request, id):
    goal_value = get_object_or_404(Goal, id=id)

    goal_value.is_completed = not goal_value.is_completed
    goal_value.save()

    return redirect("daily_goal")


@login_required
def delete_goal(request, id):
    goal = get_object_or_404(Goal, id=id)
    goal.delete()
    return redirect("daily_goal")


@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    unread_count = Notification.objects.filter(status=False).count()
    user_notifications.update(status=True)

    return render(
        request,
        "skills/notification.html",
        {"notifications": user_notifications, "unread_count": unread_count},
    )


'''@login_required
def dashboard(request):

    today = date.today()
    labels = []
    completed_data = []
    total_data = []

    for i in range(6, -1, -1):  # 6 days ago to today
        day = today - timedelta(days=i)
        day_total = Goal.objects.filter(user=request.user, created_at__date=day).count()
        day_completed = Goal.objects.filter(
            user=request.user, created_at__date=day, is_completed=True
        ).count()

        labels.append(day.strftime("%b %d"))  # format like "Jan 13"
        total_data.append(day_total)
        completed_data.append(day_completed)

    last_7_days = today - timedelta(days=7)

    # Weekly Goals
    weekly_goals = Goal.objects.filter(
        user=request.user, created_at__date__gte=last_7_days
    )
    weekly_total = weekly_goals.count()
    weekly_completed = weekly_goals.filter(is_completed=True).count()
    # weekly_pending = weekly_goals.filter(is_completed = False).count()

    """streak = 0
    check_date = today
    while True:
        completed_on_day =Goal.objects.filter(
            user = request.user,
            is_completed =True,
            created_at = check_date
        ).exists()
        if completed_on_day:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break"""

    unread = Notification.objects.filter(user=request.user, status=False).count()

    context = {
        "weekly_total": weekly_total,
        "weekly_completed": weekly_completed,
        "weekly_pending": weekly_total - weekly_completed,
        #'streak': streak,
        "labels": json.dumps(labels),
        "completed_data": json.dumps(completed_data),
        "total_data": json.dumps(total_data),
        "unread": unread,
    }

    return render(request, "skills/dashboard.html", context)'''


def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(
                request, "skills/register.html", {"error": "Password do not match!"}
            )

        if User.objects.filter(username=username).exists():
            return redirect(
                request, "skills/register.html", {"error": "Username already exists."}
            )

        user = User.objects.create_user(username=username, password=password)
        login(request, user)

        return redirect("daily_goal")
    return render(request, "skills/register.html")


def user_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            return render(
                request,
                "skills/login.html",
                {"error": "Account not found. Please register"},
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home_page")
        else:
            return render(
                request, "skills/login.html", {"error": "Invalid Username or Password."}
            )

    return render(request, "skills/login.html")


def user_logout(request):
    logout(request)
    return redirect("home_page")


def home_page(request):
    return render(request, "skills/index.html")
