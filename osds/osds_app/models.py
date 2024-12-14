from django.db import models

# Create your models here.
class Users(models.Model):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('student', 'Student'),
    ]
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    role = models.CharField(max_length=30, choices=USER_TYPE_CHOICES)
    mail = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    department = models.CharField(max_length=100)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    cpga = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    #REQUIRED_FIELDS = ['', 'user_type']

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class StudentDocumentRequest(models.Model):
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

class Invoice(models.Model):
    staff = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sent_invoices', limit_choices_to={'user_type': 'staff'})
    student = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='received_invoices', limit_choices_to={'user_type': 'student'})
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    payment_proof = models.FileField(upload_to='invoices/', blank=True, null=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.student.username} ({'Paid' if self.is_paid else 'Unpaid'})"
    
class GradeRecord(models.Model):
    student = models.ForeignKey(Users, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    gpa = models.FloatField()
    cgpa = models.FloatField()
    updated_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name='updated_grades', limit_choices_to={'user_type': 'staff'})
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} - GPA: {self.gpa}, CGPA: {self.cgpa}"