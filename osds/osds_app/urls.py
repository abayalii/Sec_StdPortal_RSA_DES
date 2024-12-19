from . import views
from django.urls import path

urlpatterns = [
    path("users/", views.login, name="login"),
    path("users/login",views.login,name="login"),
    path("users/admin",views.admin,name="admin"),
    path("users/student",views.student,name="student"),
    path("users/staff",views.staff,name="staff")
    
]
