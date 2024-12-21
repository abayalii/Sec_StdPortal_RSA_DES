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
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default='Pending')
    gpa_list = models.JSONField(null=True, blank=True)  # Store GPA values as a JSON array
    cpga = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.document_type} - {self.student.username}"
    

 
 

    