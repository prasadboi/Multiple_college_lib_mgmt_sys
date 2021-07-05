from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from library.models import College,Books
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    wallet_points = models.IntegerField(null=True)
    MEMBERSHIP_CHOICES = (
        ('G', 'Gold'),
        ('S', 'Silver'),
        ('B', 'Bronze'),
    )
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, null=True)
    first_name = models.CharField(max_length=255,null=True)
    last_name  = models.CharField(max_length=255,null=True)
    student_id = models.TextField(max_length=255,null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField(null=True)
    phone_no = models.IntegerField(null=True)
    email = models.EmailField(max_length=255,null=True)
    branch = models.CharField(max_length=255,null=True)
    College = models.ForeignKey(College,on_delete=models.CASCADE,null=True)

class issue(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    book = models.ForeignKey(Books,on_delete=models.CASCADE,null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','book'], name='book_student_cons')
        ]
    Issue_date = models.DateField(default=timezone.now)
    # Create your models here.
    Return_date = models.DateField(null=True)
class Request(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Book = models.ForeignKey(Books,on_delete=models.CASCADE)
class Admin(models.Model):
    # admin class extends user class
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # admin id - assigned by the system, thereby unique
    admin_id = models.CharField(primary_key=True, max_length=255)

    # name
    first_name = models.CharField(max_length=255,null=True)
    last_name  = models.CharField(max_length=255,null=True)
    # age
    age = models.IntegerField(null=True)
    # email id
    email = models.EmailField(max_length=255,null=True)
    phone_no = models.IntegerField(null=True)
    #gender
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    # address details of admin
    pincode = models.IntegerField(null=True)
    city = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255,null=True)

    # admin has a 1-1 total relationship with class 'College'
    college = models.OneToOneField(College,on_delete= models.CASCADE)