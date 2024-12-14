from . import views
from django.urls import path

urlpatterns = [
    path("login",views.login),
    path("admin",views.admin),
    path("student",views.student),
    path("staff",views.staff)
    
]
