from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from user import views as user_views
from task import views as task_views


urlpatterns = [

# Valyuta kursi
    path("currency/", task_views.CurrencyView.as_view(), name="currency"),

# AUTHENTICATION
    path('signup/', user_views.SignUpView.as_view(), name='signup'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('logout/', user_views.LogoutView.as_view(), name='logout'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='refresh'),
    path('black/', jwt_views.TokenBlacklistView.as_view(), name='black'),

# USER PROFILE and STATS
    path("profiles/", user_views.UserProfileListView.as_view(), name='profiles'),
    path("sector/profiles/<int:id>/", user_views.SectorEmployeeAPIView.as_view(), name='sector_profiles'),


# Sector Create Get Update
    path('sectors/', user_views.SectorCreateListView.as_view(), name='sectors'),
    path('sector/<str:pk>/', user_views.SectorDetailView.as_view(), name='sector'),

# Task Create List
    path("tasks/create/", task_views.TaskListCreateView.as_view(), name='tasks_create'),
    path("task/<str:pk>/", task_views.TaskDetailView.as_view(), name='task_detail'),
    path("manager/tasks/", task_views.ManagerTaskListView.as_view(), name='manager_tasks'),
    path("director/tasks/", task_views.DirectorTaskListCreateView.as_view(), name='director_tasks'),

# REVIEW FOR THE TASK
    path("reviews/", task_views.TaskReviewListView.as_view(), name='reviews'),
    path("review/<str:pk>/", task_views.ReviewDetailView.as_view(), name='review'),
    path("reviews/tasks/<int:id>/", task_views.TaskReviewListView.as_view(), name='reviews_for_task'),



# Each Task Review
    path("task/reviews/<int:id>/", task_views.EachTaskReview.as_view(), name='task_reviews'),


# FINISH, CANCEL TASK
    path("finish/<int:id>/", task_views.FinishTaskView.as_view(), name='finished'),
    path("cancel/<int:id>/", task_views.CancelTaskView.as_view(), name='canceled'),

    path("send/arxiv/<int:id>/", task_views.ArxivTaskView.as_view(), name='arxiv'),


# 1 - Page Barcha ko'rsatkichlar

    # STATS FOR SECTORS
    path("sectors/stats/", task_views.SectorStatView.as_view(), name='sectors_stats'),

    # STAT FOR TASKS
    path("tasks/stats/", task_views.StatView.as_view(), name='tasks_stats'),

    # stat for managers
    path("managers/stats/", user_views.ManagerStatListView.as_view(), name='manager_stats'),

    # stat for all users
    path("users/stats/", user_views.UserStatListView.as_view(), name='stats'),


# 2 - page Bo'limlar bo'yicha

    # Each sector tasks stat
    path("stats/sector/<int:id>/", task_views.EachSectorStatView.as_view(), name='each_sector_tasks'),

    # Each sector tasks
    path("tasks/sector/<int:id>/", task_views.EachSectorTasksView.as_view(), name='each_sector_tasks'),

    # Each sector employee stat
    path("employee/sector/<int:id>/", task_views.EachSectorEmployeeStatView.as_view(), name='sector_employee_stat'),


# 3 - Page Shaxsiy kabinet

    # User sector task
    path("user/sector/tasks/<int:id>/", task_views.UserSectorTasksView.as_view(), name='user_sector_tasks'),

    # User director task
    path("user/director/tasks/<int:id>/", task_views.UserDirectorTasksView.as_view(), name='user_director_tasks'),

    # profile
    path("profile/<str:pk>/", user_views.UserProfileView.as_view(), name='profile'),

    # STAT FOR USERS
    path("employees/stats/<int:id>/", user_views.EmployeeStatListView.as_view(), name='employee_stats'),


# 4 - page Request User

    # request user profile
    path("user/profile/", user_views.RequestUserProfileView.as_view(), name='request_user_profile'),
    path("user/stat/", user_views.RequestUserStatView.as_view(), name='request_user_stat'),

    # User sector task
    path("user/sector/tasks/", task_views.RequestUserSectorTasksView.as_view(), name='request_user_sector_tasks'),

    # User director task
    path("user/director/tasks/", task_views.RequestUserDirectorTasksView.as_view(), name='request_user_director_tasks'),


]



