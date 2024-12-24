from django.db import models


class Users(models.Model):
    
    username = models.CharField(max_length=30, unique=True)
    student_number = models.CharField(max_length=30, null=True, blank=True,unique=True)
    name=models.CharField(max_length=30)
    surname=models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=30)
    mail = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    department = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username
    


    
class Documents(models.Model):
    student = models.ForeignKey(Users, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=30,default='transcript')
    invoice_file = models.FileField(upload_to='./documents/invoices/',null=True,blank=True)
    receipt_file = models.FileField(upload_to='./documents/receipts/', null=True, blank=True)
    document_file = models.FileField(upload_to='./documents/docs/', null=True, blank=True)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default='Pending')
    gpa_list = models.JSONField(null=True, blank=True)  # Store GPA values as a JSON array
    cpga = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    signature = models.TextField(null=True)  # Store the signature
    signature_data = models.TextField(null=True)  # Store the data that was signed
    receipt_signature=models.TextField(null=True)
    receipt_signature_data=models.TextField(null=True)
    is_verified = models.BooleanField(default=False)  # Flag for verification status
    is_receipt_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.document_type} - {self.student.username}"
    


class Rsa(models.Model):
    public_key=models.CharField(max_length=200)
    private_key=models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.public_key} - {self.private_key}"
 

    