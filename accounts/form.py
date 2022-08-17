from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from accounts.models import User, issue
from django.db import transaction

from accounts.models import Student
from library.models import College, Books


class Student_Form(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    student_id = forms.CharField(required=True)
    colleges_obj = list(College.objects.all())
    college = []
    for i in colleges_obj:
        college.append([i.College_id,i.College_id])
    college_tuple = tuple(tuple(i) for i in college)
    College_id = forms.ChoiceField(choices=college_tuple,required=True)
    MEMBERSHIP_CHOICES = (
        ('G', 'Gold'),
        ('S', 'Silver'),
        ('B', 'Bronze'),
    )

    membership = forms.ChoiceField(choices=MEMBERSHIP_CHOICES,required=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES,required=True)
    age = forms.IntegerField(required=True)
    phone_no = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)
    branch = forms.CharField()
    class Meta(UserCreationForm.Meta):
        model = User
    def clean(self):
        data = self.cleaned_data
        student_id = self.cleaned_data.get('student_id')
        college_id = self.cleaned_data.get('College_id')
        c = Student.objects.filter(College_id=college_id, student_id=student_id).count()
        if (c > 0):
            self.add_error('student_id',"Student already exists")
        return data
    @transaction.atomic
    def save_data(self):
        Wallet = {
            'G': 1000,
            'S': 500,
            'B': 250,
        }
        user = super().save(commit=False)
        mem = self.cleaned_data.get('membership')

        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.membership = mem
        student.wallet_points = Wallet.get(mem)
        student.first_name = self.cleaned_data.get('first_name')
        student.last_name = self.cleaned_data.get('last_name')
        student.student_id = self.cleaned_data.get('student_id')
        id = str(self.cleaned_data.get('College_id'))

        obj = College.objects.get(College_id=id)

        student.College_id = obj
        student.gender = self.cleaned_data.get('gender')
        student.age = self.cleaned_data.get('age')
        student.phone_no = self.cleaned_data.get('phone_no')
        student.email = self.cleaned_data.get('email')
        student.branch = self.cleaned_data.get('branch')
        student.save()
        return user
class update_profile(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)

    age = forms.IntegerField(required=False)
    phone_no = forms.IntegerField(required=False)
    email = forms.EmailField(required=False)
    branch = forms.CharField(required=False)