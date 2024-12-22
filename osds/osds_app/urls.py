from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.login, name="login"),
    path("users/admin/",views.admin,name="admin"),
    path('users/add-staff/', views.add_staff, name='add_staff'),
    path('users/add-student/', views.add_student, name='add_student'),
    path("users/student/",views.student,name="student"),
    path('users/request-document',views.request_document,name="request_document"),
    path("users/staff/",views.staff,name="staff"),
    path("users/update-des-key/",views.update_des_key,name="update_des_key"),
    path("users/pending-requests",views.pending_requests,name="pending_requests"),
    path("users/logout/",views.logout,name="logout")
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

