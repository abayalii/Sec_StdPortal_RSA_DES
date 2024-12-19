from django.db import models
from .utils.des import encrypt_des


class Users(models.Model):
    ROLE_CHOICES = [
        ('staff', 'Staff'),
        ('admin', 'Admin'),
        ('student', 'Student')
    ]
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    mail = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    department = models.CharField(max_length=100)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    cpga = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Users'  # Fixed plural name

    def save(self, *args, **kwargs):
        if self.role != 'student':
            self.gpa = None
            self.cpga = None
            
        request = kwargs.pop('request', None)
        if request and 'des_key' in request.session:
            des_key = request.session['des_key'].encode()
            self.username = encrypt_des(self.username, des_key)
            self.password = encrypt_des(self.password, des_key)
            if self.mail:
                self.mail =encrypt_des(self.mail, des_key)
            if self.phone:
                self.phone = encrypt_des(self.phone, des_key)
            if self.department:
                    self.department = encrypt_des(self.department, des_key)
        
        super().save(*args, **kwargs)

    #def __str__(self):
        #return f"{self.username} ({self.get_role_display()})"  # Fixed method name

    
class Documents(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('certificate', 'Student Certificate'),
        ('transcript', 'Transcript'),
    ]

    student = models.ForeignKey(Users, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    
    def __str__(self):
        return f"{self.student.username} - {self.get_document_type_display()} ({self.status})"

 
 
class Invoices(models.Model):
    staff = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sent_invoices', limit_choices_to={'user_type': 'staff'})
    student = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='received_invoices', limit_choices_to={'user_type': 'student'})
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    payment_proof = models.FileField(upload_to='invoices/', blank=True, null=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.student.username} ({'Paid' if self.is_paid else 'Unpaid'})"
    