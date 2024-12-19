from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils.des import decrypt_des
from .models import Users



import logging
logger=logging.getLogger('osds_app')

# Create your views here.

def login(request):
    
    if request.method == "POST":
        logger.debug(f"POST data: {request.POST}")
        username = request.POST.get("username")
        password = request.POST.get("password")
        des_key = request.POST.get("des_key")
        
        logger.info(f"Login attempt for username: {username}")
        
        if not all([username, password, des_key]):
            logger.warning("Missing required fields in login attempt")
            messages.error(request, "All fields are required")
            return render(request, "login.html")

        
        try:
            users=Users.objects.all()
            for user in users:
                try:
                    decrypted_username = decrypt_des(des_key.encode(), user.username)
                    if decrypted_username == username:
                        decrypted_password = decrypt_des(des_key.encode(), user.password)
                        if decrypted_password == password:
                            logger.info(f"Successful login for user: {username} with role: {user.role}")
                            request.session['des_key'] = des_key
                            request.session['user_id'] = user.id
                            request.session['role'] = user.role
                            if user.role == 'admin':
                                return redirect('admin')
                            elif user.role == 'student':
                                return redirect('student')
                            else:
                                return redirect('staff')
            
                except Exception as e:
                    logger.error(f"Decryption error for user {user.id}: {str(e)}")
                    continue
        

            logger.warning(f"Failed login attempt for username: {username}")
            messages.error(request, "Invalid credentials")
            return render(request, "login.html")

        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            messages.error(request, "An error occurred")
            return render(request, "login.html")

    return render(request, "login.html")
   


@login_required
def admin(request):
    logger.debug(f"Session data: {request.session}")
    if request.session.get('role') != 'admin':
        return redirect('login')
    return render(request, "admin.html")


def student(request):
    
    return render(request, "student.html")


def staff(request):
    
    return render(request, "staff.html")