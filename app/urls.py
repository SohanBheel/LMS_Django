from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.home, name="home"),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('profile/', views.profile, name='profile'),
    path('profile/<int:id>/', views.view_profile, name='view_profile'),
    path('profile/<int:id>/', views.view_profile, name='view_profile'),
    path('usersearch/', views.usersearch, name='usersearch'),
    path('removeenrollment/<int:id>/', views.removeenrollment, name='view_profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('create_course/', views.create_course, name='create_course'),
    path('view_course/<int:course_id>/', views.view_course, name='view_course'),
    path('search/', views.search, name='search'),
    path('forum/', views.forum, name='forum'),
    path('feedback_support/<int:course_id>/', views.feedback_support, name='facebook_support'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('enroll/<int:course_id>/', views.enroll_now, name='enroll_now'),
    path('upload_material/<int:course_id>/', views.upload_material, name='upload_material'),
    path('upload_material/<int:course_id>/', views.upload_material, name='upload_material'),
    path('students/<int:course_id>/', views.view_students, name='view_students'),
    path('view_material/<int:course_id>/', views.view_material, name='view_material'),
    path('notifications/', views.notifications, name='notifications'),
    path('writeupdates/', views.writeupdates, name='writeupdates'),
    path('deleteupdate/<int:id>/', views.deleteupdate, name='deleteupdate'),
]