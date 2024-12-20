from . import views
from django.urls import path

urlpatterns = [
    path("users/", views.login, name="login"),
    path("users/admin/",views.admin,name="admin"),
    path("users/student/",views.student,name="student"),
    path("users/staff/",views.staff,name="staff"),
    path("users/logout/",views.logout,name="logout")
    
]
