from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("users/", views.login, name="login"),
    path("users/admin/",views.admin,name="admin"),
    path('users/add-staff/', views.add_staff, name='add_staff'),
    path('users/add-student/', views.add_student, name='add_student'),
    path("users/student/",views.student,name="student"),
    path('users/request-document',views.request_document,name="request_document"),
    path("users/staff/",views.staff,name="staff"),
    path("users/pending-requests",views.pending_requests,name="pending_requests"),
    path("users/logout/",views.logout,name="logout")
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
