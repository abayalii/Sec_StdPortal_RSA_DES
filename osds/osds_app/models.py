from django.db import models


class Users(models.Model):
    
    username = models.CharField(max_length=30)
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
    document_type = models.CharField(max_length=30)
    request_date = models.DateTimeField(auto_now_add=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    cpga = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.document_type} - {self.student.username}"
    

 
 

    