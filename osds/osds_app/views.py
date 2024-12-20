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
                print(f"Session ID: {request.session.get('id')}")
                print(f"Session Username: {request.session.get('username')}")
                
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





def admin(request):
    id = request.session.get('id')  # Oturumdaki kullanıcı ID'sini al
    username = request.session.get('username')  # Oturumdaki kullanıcı adını al
    print(f"Admin Page Accessed by User: {username} (ID: {id})")
    
    if not id:
        return redirect("login")  # Kullanıcı oturum açmamışsa login sayfasına yönlendirme

    
    return render(request, "admin.html",{"username": username})

def student(request):
    
    return render(request, "student.html")


def staff(request):
    
    return render(request, "staff.html")


def logout(request):
    # Oturum verilerini temizle
    request.session.flush()
    return redirect("login")