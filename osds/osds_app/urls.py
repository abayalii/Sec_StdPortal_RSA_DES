from . import views
from django.urls import path

urlpatterns = [
    path("users/", views.login, name="login"),
    path("users/admin/",views.admin,name="admin"),
    path('users/add-staff/', views.add_staff, name='add_staff'),
    path('users/add-student/', views.add_student, name='add_student'),
    path("users/student/",views.student,name="student"),
    path("users/staff/",views.staff,name="staff"),
    path("users/logout/",views.logout,name="logout")
    
]
