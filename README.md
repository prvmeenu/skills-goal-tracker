#Skill & Goal Tracker (Full stack Django)
A professional personal development web app to manage learning paths and track daily progress.

##Project Overview
This application serves as a centralized hub for users to define long-term Skills and break them down into actionable Daily Goals. It features a robust authentication system, real-time progress visualization, and a modern, responsive interface.

##Key Features
User Authentication: Secure Sign-up, Login and Logout functionalitiy using Django's built in Auth system.
Skills Tracking: Create, Edit and Delete skills with star ratings (1-10).
Goal Tracking: Add, Edit, Toggle and Delete Goals with progress tracking.
Smart filtering: View goals by status (All, Complete, Pending) using optimized Django Querysets.
Dynamic Progress Bar: A Boostrap-powered progress bar that calculate completion percentage based on current filter.
In-App Notification: Automatic notifications using Django signals.
Responsive-UI: styled with Bootstrap 5

##Technical Stack
Backend: Python/Django
Frontend: Django Template Language, Bootstrap
Database : SQLite
Security: CSRF protection on all forms and @login_required decorators to protect user data.

##Installation & setup
Clone the repository:

Bash
git clone [https://github.com/yourusername/skill-goal-tracker.git](https://github.com/prvmeenu/skills-goal-tracker)
cd skill-goal-tracker
Set up Virtual Environment:

Bash
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
Install Dependencies:

Bash
pip install django
Run Migrations & Start Server:

Bash
python manage.py migrate
python manage.py runserver
Access the app at http://127.0.0.1:8000

##UI Showcase
The Dashboard
A clean bootstrap interface displaying the user's active skills and filtered view of daily goals.

##Pages
Page Description,
Home - Landing page with app features.
Register - Create a new account
Login - Login to your account
Skills - Add and manage your skills
Daily Goals - Add, complete and track daily goals
Notifications - View all in-app notifications

##Notification working
Notifications are triggered automatically using Django Signals:

New skill added →"New skill added: Python"
New goal added → "New goal added: Exercise"
Goal completed → "Goal completed: Exercise"

##Challenges Overcome
1.Model Realtionship issue:
problem: Data was not being saved in the database.
solution: identified missing migration. Connected model using blank=TRUE, null=True only for creation then change it to false after creation.

2.Filter Function Not Working:
problem: Filter links update the url but not call the correct view.
solution: Used proper Django template syntax. Ensured view handle query parameters correctly.

3.Toggle & Filter logic issue:
problem: Goal status changes were not reflected in filtered result
solution: Ensured boolean values(True/false) instead of strings.

4.Edit form not showing existing data:
problem: Edit page appeared like a new form instead of showing the saved values
solution: used condition for checkbox.

##Author
Meenakshi veerappan
