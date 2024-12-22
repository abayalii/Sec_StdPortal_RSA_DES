from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .utils.des import decrypt_des,encrypt_des
from .utils.rsa import rsa_sign,rsa_verify,generate_rsa_key_pair
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from .models import Users, Documents,Rsa
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io



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

@role_required(['admin'])  # Only admins can add student
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
    des_key = request.session.get('des_key')
    print(f"DES Key from session: {des_key}")
    if not des_key:
        return render(request, "staff.html", {"error": "DES key is required to decrypt data."})

    try:
        print(f"Fetching invoices for student ID: {id}")
        # Fetch the invoices for the student
        invoices = Documents.objects.filter(student_id=id).exclude(invoice_file__isnull=True)  # Assuming invoice field in Documents
        print(f"Number of invoices found: {invoices.count()}")
        decrypted_invoices = []

        for invoice in invoices:
            print(f"Processing invoice ID: {invoice.id}")
            print(f"Invoice file path: {invoice.invoice_file.name if invoice.invoice_file else 'No file'}")
            print(f"Document type: {invoice.document_type}")
            print(f"Signature present: {'Yes' if invoice.signature else 'No'}")
            print(f"Signature data present: {'Yes' if invoice.signature_data else 'No'}")
            
            decrypted_invoices.append({
                "id": invoice.id,
                "document_type": decrypt_des(des_key, invoice.document_type),
                "status": "Verified" if invoice.is_verified else "Not Verified",
                "url": invoice.invoice_file.url,  # Assuming FileField for invoices
                "signature": invoice.signature,  # Add signature
                "signature_data": invoice.signature_data # Add signature data
            })
        
        if request.method == 'POST':
            # Handle form submission for verification
            document_id = request.POST.get('document_id')
            print(f"Verification requested for document ID: {document_id}")
            signature = request.POST.get('signature')
            signature_data = request.POST.get('signature_data')

            try:
                document = Documents.objects.get(id=document_id)

                # Fetch the RSA public key
                rsa_keys = Rsa.objects.first()
                if not rsa_keys:
                    return render(request, "student.html", {"error": "RSA keys not found."})
                public_key = rsa_keys.public_key
                
                if not document.signature or not document.signature_data:
                    raise Exception("Signature or signature data missing")
                print(f"Verifying signature with data: {document.signature_data}")

                # Verify the signature
                if rsa_verify(document.signature_data, document.signature, public_key):
                    document.is_verified = True
                    document.save()
                    return redirect('student')  # Refresh page after verification
                else:
                    print("Signature verification failed")
                    raise Exception("Invalid signature")
            except Documents.DoesNotExist:
                print(f"Document not found: {document_id}")
                return render(request, "student.html", {
                    "error": "Document not found.",
                    "username": username,
                    "invoices": decrypted_invoices
                })
            except Exception as e:
                print(f"Verification error: {str(e)}")
                return render(request, "student.html", {
                    "error": f"Verification failed: {str(e)}",
                    "username": username,
                    "invoices": decrypted_invoices
                })

        print(f"Rendering template with {len(decrypted_invoices)} invoices")
        return render(request, "student.html", {
            "username": username,
            "invoices": decrypted_invoices
        })

    except Exception as e:
        print(f"Error in student view: {str(e)}")
        return render(request, "student.html", {
            "error": f"Error processing invoices: {str(e)}",
            "username": username
        })
        
            

        
        #return render(request, "student.html", {
            #"username": username,
            #"invoices": decrypted_invoices
        
    except Exception as e:
        print(f"Error fetching invoices: {e}")
        return render(request, "student.html", {"error": "Error fetching invoices."})
    
    
    print(f"Student Page Accessed by User: {username} (ID: {id})")
    
    if not id:
        return redirect("login")  # Kullanıcı oturum açmamışsa login sayfasına yönlendirme
    
    return render(request, "student.html",{"username": username})

@role_required(['student'])
def request_document(request):
    if request.method == 'POST':
        des_key = request.POST.get('des_key')
        if not des_key:
            print("des key not found")
            return render(request, "student.html", {"error": "DES key is required to encrypt data."})
        
        document_type = request.POST.get('document-type')
        student_id = request.session.get('id')# Logged-in student's ID
        print(f"Document Type: {document_type}, Student ID: {student_id}")
        
        try:
            student = Users.objects.get(id=student_id)

            # Encrypt document request details
            encrypted_document_type = encrypt_des(des_key, document_type)
            encrypted_status = encrypt_des(des_key, "Pending")
            print(f"Encrypted Document Type: {encrypted_document_type}, Status: {encrypted_status}")
            document=Documents.objects.create(
                student=student,
                document_type=encrypted_document_type,
                status=encrypted_status
            )
            print(f"Document {document.id} created successfully")

            return render(request, "student.html", {"success": "Document request submitted successfully!"})
            
        except Users.DoesNotExist:
            return render(request, "student.html", {"error": "Student not found."})
        except Exception as e:
            return render(request, "student.html", {"error": f"Error submitting request: {e}"})
            
    
    return redirect('student')

@role_required(['student'])
def submit_receipt(request):
    
    return redirect('student')

@role_required(['staff'])
def staff(request):
    
    return render(request, "staff.html")

@role_required(['staff'])
def pending_requests(request):
        des_key = request.session.get('des_key')
        print(f"DES Key from session: {des_key}")
        if not des_key:
            return render(request, "staff.html", {"error": "DES key is required to decrypt data."})

        try:
            encrypted_pending_status = encrypt_des(des_key, "Pending")
            print(f"Encrypted status for 'Pending': {encrypted_pending_status}")
            
            pending_requests = Documents.objects.filter(status=encrypted_pending_status)
            print(f"Fetched {len(pending_requests)} pending requests.")
            
            if request.method == 'POST':
                # Handle document preparation or invoice sending
                action = request.POST.get('action')
                request_id = request.POST.get('request_id')
                print(f"request id:{request_id}")
                
                if action == 'prepare':
                    # Add logic for preparing document
                    pass
                elif action == 'invoice':
                    try:
                        document = Documents.objects.get(id=request_id)
                        print(f"Document found: {document.id}, Type={repr(document.document_type)}")
                        student = document.student
                        
                    
                        # Determine price
                        if document.document_type == encrypt_des(des_key,"transcript"):
                            print(f"document type:{document.document_type}")
                            price = 200
                        elif document.document_type == encrypt_des(des_key,"certificate"):
                            print(f"document type:{document.document_type}")
                            price = 50
                        else:
                            price = 100  # Default price
                        
                        # Fetch RSA private key
                        rsa_keys = Rsa.objects.first()# Adjust as needed
                        if not rsa_keys:
                            private_key, public_key = generate_rsa_key_pair()
                            rsa_keys = Rsa.objects.create(
                                private_key=private_key,
                                public_key=public_key
                            )
                        private_key = rsa_keys.private_key
                        
                        # Generate invoice
                        buffer,signature,signature_data = generate_invoice(
                            student_name=decrypt_des(des_key, student.name),
                            student_surname=decrypt_des(des_key, student.surname),
                            student_number=decrypt_des(des_key, student.student_number),
                            document_type=decrypt_des(des_key, document.document_type),
                            price=price,
                            private_key=private_key
                        )
                        
                        # Save invoice to a file
                        fs = FileSystemStorage()
                        filename = f"invoice_{document.id}.pdf"
                        file_path = fs.save(f"invoices/{filename}", buffer)
                        document.invoice_file = file_path
                        document.signature=signature
                        document.signature_data=signature_data
                        
                        document.save()  # Save the file reference to the database
                        
                        # Update database or notify student as needed
                        
                        return render(request, "staff.html", {"message": "Invoice sent successfully."})
                    except Documents.DoesNotExist:
                        print(f"Document with ID {request_id} does not exist.")
                        return render(request, "staff.html", {"error": "Document not found."})
                
            decrypted_requests = []
            for req in pending_requests:
                student = req.student  # Fetch the related student object via ForeignKey

                decrypted_requests.append({
                    "student_name": decrypt_des(des_key, student.name),
                    "student_surname": decrypt_des(des_key, student.surname),
                    "student_number": decrypt_des(des_key, student.student_number),
                    "document_type": decrypt_des(des_key, req.document_type),
                    "status": decrypt_des(des_key, req.status),
                    "request_date": req.request_date.strftime('%Y-%m-%d %H:%M:%S'),
                    "id": req.id  # Include request ID for further actions
                })
            print(f"Decrypted Requests: {decrypted_requests}")

            return render(request, "staff.html", {"requests": decrypted_requests})
        except Exception as e:
            print(f"Error: {e}")
            return render(request, "staff.html", {"error": f"Error fetching pending requests: {e}"})


def generate_invoice(student_name, student_surname, student_number, document_type, price, private_key):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Invoice")
    c.drawString(100, 730, f"Student Name: {student_name} {student_surname}")
    c.drawString(100, 710, f"Student Number: {student_number}")
    c.drawString(100, 690, f"Document Type: {document_type}")
    c.drawString(100, 670, f"Price: ${price}")
    
    # Generate signature
    data = f"{student_name} {student_surname} {student_number} {document_type} {price}"
    signature = rsa_sign(data, private_key)
    c.drawString(100, 650, f"Digital Signature: {signature}...")
    
    c.save()
    buffer.seek(0)
    return buffer,signature,data

    
    
    
    
  


def logout(request):
    # Oturum verilerini temizle
    request.session.flush()
    return redirect("login")