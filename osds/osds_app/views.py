from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils.des import decrypt_des,encrypt_des
from .models import Users



def login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        des_key = request.POST.get('des_key')
        
        if not all([username, password, des_key]):
            
            return render(request, "login.html",{"error": "Lütfen tüm alanları doldurun."})
        
        try:
            encrypted_username = encrypt_des(des_key, username)
            print(f"Encrypted Username: {encrypted_username}")
            
            user=Users.objects.get(username=encrypted_username)
            
            encrypted_password= encrypt_des(des_key,password)
            
            print(f"Encrypted Password (Login): {encrypted_password}")
            print(f"Database Password (Encrypted): {user.password}")
            
            
            
            if (user.username==encrypted_username) and (user.password==encrypted_password):
                decrypted_role=decrypt_des(des_key,user.role)
                print(f"Decrypted Role: {decrypted_role}")
                
                request.session['id'] = user.id
                request.session['username'] = user.username 
                request.session['role'] = decrypted_role
                request.session['des_key']=des_key 
                
                print(f"Session ID: {request.session.get('id')}")
                print(f"Session Username: {request.session.get('username')}")
                print(f"Session DES KEY: {request.session.get('des_key')}")
                
                if decrypted_role == "admin":
                  return redirect("admin")
                elif decrypted_role == "staff":
                   return redirect("staff")
                elif decrypted_role=="student":
                    return redirect("student")
                else:
                    return render(request,"login.html",{"error":"no match role"})
                   
        except Users.DoesNotExist:
            return render(request, "login.html", {"error": "Kullanıcı bulunamadı."})
        
    return render(request, "login.html")


def role_required(allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Get the user's role from the session
            user_role = request.session.get('role')
            if not user_role or user_role not in allowed_roles:
                return HttpResponse("Access Denied", status=403)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@role_required(['admin'])
def admin(request):
    id = request.session.get('id')  # Oturumdaki kullanıcı ID'sini al
    username = request.session.get('username')# Oturumdaki kullanıcı adını al
    
    
    print(f"Admin Page Accessed by User: {username} (ID: {id})")
    
    if not id:
        return redirect("login")  # Kullanıcı oturum açmamışsa login sayfasına yönlendirme
    
    

    
    return render(request, "admin.html",{"username": username})

@role_required(['admin'])  # Only admins can add staff
def add_staff(request):
    if request.method == 'POST':
        des_key = request.POST.get('des_key')
        if not des_key:
            print("des key not found")
            return render(request, "admin.html", {"error": "DES key is required to encrypt data."})

        try:
            # Extract form data
            username = request.POST.get('staff-username')
            name = request.POST.get('staff-name')
            surname = request.POST.get('staff-surname')
            password = request.POST.get('staff-password')
            email = request.POST.get('staff-email', '')
            phone = request.POST.get('staff-phone', '')
            department = request.POST.get('staff-department')
            
            print(f"Username: {username}, Name: {name}, Surname: {surname}, Password: {password}, Department: {department}")
            
             # Validate data
            if not all([username, name, surname, password, department]):
                print("Validation failed: Missing required fields")
                return render(request, "admin.html", {"error": "Please fill in all required fields."})

            # Encrypt the data
            encrypted_username = encrypt_des(des_key, username)
            encrypted_name = encrypt_des(des_key, name)
            encrypted_surname = encrypt_des(des_key, surname)
            encrypted_password = encrypt_des(des_key, password)
            encrypted_role = encrypt_des(des_key, "staff")
            encrypted_email = encrypt_des(des_key, email) if email else ''
            encrypted_phone = encrypt_des(des_key, phone) if phone else ''
            encrypted_department = encrypt_des(des_key, department)
            
            print(f"Encrypted Username: {encrypted_username}, Encrypted Password: {encrypted_password}, Encrypted Role: {encrypted_role}")

            # Save to the database
            user=Users.objects.create(
                username=encrypted_username,
                name=encrypted_name,
                surname=encrypted_surname,
                password=encrypted_password,
                role=encrypted_role,
                mail=encrypted_email,
                phone=encrypted_phone,
                department=encrypted_department,
            )
            print(f"User {user.id} created successfully")

            return render(request, "admin.html", {"success": "Staff added successfully!"})
        except Exception as e:
            print(f"Error: {str(e)}")
            return render(request, "admin.html", {"error": f"Error adding staff: {e}"})
    return redirect("admin")

@role_required(['admin'])  # Only admins can add staff
def add_student(request):
    if request.method == 'POST':
        des_key = request.POST.get('des_key')
        if not des_key:
            print("des key not found")
            return render(request, "admin.html", {"error": "DES key is required to encrypt data."})

        try:
            # Extract form data
            student_number=request.POST.get('student-number','')
            username = request.POST.get('student-username')
            name = request.POST.get('student-name')
            surname = request.POST.get('student-surname')
            password = request.POST.get('student-password')
            email = request.POST.get('student-email', '')
            phone = request.POST.get('student-phone', '')
            department = request.POST.get('student-department')
            
            print(f"Username: {username}, Name: {name}, Surname: {surname}, Password: {password}, Department: {department}")
            
             # Validate data
            if not all([username, name, surname, password, department]):
                print("Validation failed: Missing required fields")
                return render(request, "admin.html", {"error": "Please fill in all required fields."})

            # Encrypt the data
            encrypted_student_number = encrypt_des(des_key, student_number) if student_number else ''
            encrypted_username = encrypt_des(des_key, username)
            encrypted_name = encrypt_des(des_key, name)
            encrypted_surname = encrypt_des(des_key, surname)
            encrypted_password = encrypt_des(des_key, password)
            encrypted_role = encrypt_des(des_key, "student")
            encrypted_email = encrypt_des(des_key, email) if email else ''
            encrypted_phone = encrypt_des(des_key, phone) if phone else ''
            encrypted_department = encrypt_des(des_key, department)
            
            print(f"Encrypted Username: {encrypted_username}, Encrypted Password: {encrypted_password}, Encrypted Role: {encrypted_role}")

            # Save to the database
            user=Users.objects.create(
                student_number=encrypted_student_number,
                username=encrypted_username,
                name=encrypted_name,
                surname=encrypted_surname,
                password=encrypted_password,
                role=encrypted_role,
                mail=encrypted_email,
                phone=encrypted_phone,
                department=encrypted_department,
            )
            print(f"User {user.id} created successfully")

            return render(request, "admin.html", {"success": "Student added successfully!"})
        except Exception as e:
            print(f"Error: {str(e)}")
            return render(request, "admin.html", {"error": f"Error adding student: {e}"})
    return redirect("admin")

@role_required(['student'])
def student(request):
    id = request.session.get('id')  # Oturumdaki kullanıcı ID'sini al
    username = request.session.get('username')# Oturumdaki kullanıcı adını al
    
    
    print(f"Student Page Accessed by User: {username} (ID: {id})")
    
    if not id:
        return redirect("login")  # Kullanıcı oturum açmamışsa login sayfasına yönlendirme
    
    

    
    return render(request, "student.html",{"username": username})


@role_required(['staff'])
def staff(request):
    
    return render(request, "staff.html")


def logout(request):
    # Oturum verilerini temizle
    request.session.flush()
    return redirect("login")