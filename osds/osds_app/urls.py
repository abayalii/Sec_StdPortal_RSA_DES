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
    path('users/submit-receipt/', views.submit_receipt, name='submit_receipt'),
    path('users/verify-receipt/', views.verify_receipt, name='verify_receipt'),
    path('view_receipts/', views.view_receipts, name='view_receipts'),
    path('users/request-document',views.request_document,name="request_document"),
    path("users/staff/",views.staff,name="staff"),
    path("users/update-des-key/",views.update_des_key,name="update_des_key"),
    path("users/update-rsa-keys/",views.update_rsa_keys,name="update_rsa_keys"),
    path("users/pending-requests",views.pending_requests,name="pending_requests"),
    path("users/logout/",views.logout,name="logout")
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

