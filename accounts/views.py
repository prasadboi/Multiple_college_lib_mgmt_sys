from datetime import timedelta

from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone
from django.views.generic import CreateView
from django.forms import ValidationError
from library.models import College, Books, Inventory
from .form import Student_Form, update_profile
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import User, Student, issue, Request, Admin
from django.forms import forms

def register(request):
    return render(request, '../templates/register.html')

#class customer_register(CreateView):
    #model = User
    #form_class = Student_Form
    #template_name = '../templates/customer_register.html'

    #def form_valid(self, form):

        #user = form.save()

        #login(self.request, user)
        #return redirect('/')
def student_regview(request):
    context = {}
    if(request.POST):
        form = Student_Form(request.POST)

        if(form.is_valid()):


            user = form.save_data()
            login(request,user)
            return redirect('/student_home')
    else:
        form = Student_Form()

    return render(request,'../templates/customer_register.html',{'form':form})
def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                if(user.is_student):
                    return redirect('/accounts/student_home')
                else:
                    return redirect('/accounts/admin_home')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/login.html',
    context={'form':AuthenticationForm()})
@login_required
def student_homeView(request):
    user = request.user
    issue.objects.filter(user=user,Return_date__lt=timezone.now().date()).delete()
    books1 = issue.objects.filter(user=user)

    l = books1.values_list('book_id',flat=True)
    books = Books.objects.filter(Book_id__in=l)
    for i in books:
        i.issue_date = issue.objects.get(user=user,book=i).Issue_date
        i.return_date = issue.objects.get(user=user,book=i).Return_date
    context = {
        'books': books,

    }
    return render(request,'../templates/student_home.html',context)
@login_required
def logout_view(request):
   logout(request)
   return redirect('/accounts/login')
@login_required
def contact_us(request):
    return redirect('/accounts/contact')
@login_required
def contact_view(request):
    return render(request,'../templates/contact.html')
@login_required
def profile_btn(request):
    return redirect('/accounts/profile')
@login_required
def profile(request):
    user = request.user
    student = Student.objects.get(user=user)
    context = {
        'user': user,
        'student': student
    }
    return render(request,'../templates/profile.html',context)
@login_required
def edit(request):
    return redirect('/accounts/edit_profile')
@login_required
def edit_view(request):
    if(request.POST):
        form = update_profile(request.POST)
        if(form.is_valid()):
            user = request.user
            student = Student.objects.get(user=user)

            if(form.cleaned_data.get('first_name')!=''):
                first_name = form.cleaned_data.get('first_name')
                student.first_name = first_name
            if(form.cleaned_data.get('last_name')!=''):
                last_name = form.cleaned_data.get('last_name')
                student.last_name = last_name
            if(form.cleaned_data.get('gender')!=None):
                gender = form.cleaned_data.get('gender')
                student.gender = gender
            if(form.cleaned_data.get('age')!=None):
                age = form.cleaned_data.get('age')
                student.age = age
            if(form.cleaned_data.get('phone_no')!=None):
                phone = form.cleaned_data.get('phone_no')
                student.phone_no = phone
            if(form.cleaned_data.get('email')!=''):

                email = form.cleaned_data.get('email')
                student.email = email

            if(form.cleaned_data.get('branch')!=''):
                branch = form.cleaned_data.get('branch')
                student.branch = branch
            student.save()
            return redirect('/accounts/profile')


    return render(request,'../templates/edit_view.html',{'form':update_profile()})
@login_required
def return_book(request):
    return redirect('/accounts/return_book_page')
@login_required
def return_book_page(request):
    user = request.user
    books1 = issue.objects.filter(user=user)
    l = books1.values_list('book_id', flat=True)
    books = Books.objects.filter(Book_id__in=l)
    context = {
        'books': books
    }
    if(request.POST):
        book_id = request.POST.get('optradio')
        student = Student.objects.get(user=user)
        college = student.College
        if(book_id!=None):
            book = Books.objects.get(Book_id=book_id)
            invt = Inventory.objects.get(College=college,Books=book)
            invt.Book_count = invt.Book_count + 1
            invt.save()
            issue.objects.get(user=user,book=book).delete()
        return redirect('/accounts/student_home')
    return render(request,'../templates/return_book.html',context)
@login_required
def add_book(request):
    return redirect('/accou'
                    'nts/add_book_page');
@login_required
def add_book_page(request):
    user = request.user
    #user1 = User.objects.get(username=user.username)
    student = Student.objects.get(user=user)
    college = student.College
    college_invt = Inventory.objects.filter(College=college,Book_count__gt=0).values_list('Books_id',flat=True)
    student_books = issue.objects.filter(user=user).values_list('book_id',flat=True)
    books_id = [i for i in college_invt if i not in student_books]
    books = Books.objects.filter(Book_id__in=books_id)



    context = {
        'books':books
    }
    if(request.POST):
        book_id = request.POST.get('optradio')
        if(book_id!=None):
            book = Books.objects.get(Book_id=book_id)
            count = issue.objects.filter(user=user,Issue_date=timezone.now().date()).count()
            if(student.membership == 'G'):
                if(count == 5):
                    messages.error(request,"Already did 5 issues today")
                    return redirect('/accoounts/student_home')
            if(student.membership == 'S'):
                if(count == 3):
                    messages.error(request, "Already did 3 issues today")
                    return redirect('/accoounts/student_home')
            if(student.membership == 'B'):
                if (count == 1):
                    messages.error(request, "Already did 1 issue today")
                    return redirect('/accoounts/student_home')
            if(int(book.Price_points) > student.wallet_points ):
                messages.error(request,"Not enough wallet points please buy new membership for more wallet points")
                return redirect('/accounts/student_home')
            else:
                issue_date = timezone.now().date()
                if(student.membership == 'G'):
                    return_date = issue_date + timedelta(days=30)
                elif(student.membership == 'S'):
                    return_date = issue_date + timedelta(days=20)
                else:
                    return_date = issue_date + timedelta(days=10)

                i = issue(user=user,book=book,Issue_date=issue_date,Return_date=return_date)
                i.save()
                intv = Inventory.objects.get(College=college,Books_id=book_id)
                intv.Book_count = intv.Book_count - 1
                intv.save()
                student.wallet_points = student.wallet_points - int(book.Price_points)
                student.save()
        return redirect('/accounts/student_home')
    return render(request,'../templates/add_book.html',context)
@login_required
def membership(request):
    return redirect('/accounts/membership_page')
@login_required
def membership_page(request):
    if(request.POST):
        if(request.POST.get('btn')):
            user = request.user
            student = Student.objects.get(user=user)
            student.membership = 'G'
            student.wallet_points = student.wallet_points + 1000
            student.save()
            return redirect('/accounts/student_home')
        elif(request.POST.get('btn1')):
            user = request.user
            student = Student.objects.get(user=user)
            student.membership = 'S'
            student.wallet_points = student.wallet_points + 500
            student.save()
            return redirect('/accounts/student_home')
        elif(request.POST.get('btn2')):
            user = request.user
            student = Student.objects.get(user=user)
            student.membership = 'B'
            student.wallet_points = student.wallet_points + 200
            student.save()
            return redirect('/accounts/student_home')
        else:
            return redirect('/accounts/student_home')
    return render(request,'../templates/membership.html')
@login_required
def request_book(request):
    return redirect('/accounts/request_book_page')
@login_required
def request_book_page(request):
    user = request.user
    student = Student.objects.get(user=user)
    college = student.College
    all_books = Books.objects.all().values_list('Book_id',flat=True)
    student_books = issue.objects.filter(user=user).values_list('book_id', flat=True)
    college_books = Inventory.objects.filter(College=college,Book_count__gt=0).values_list('Books_id',flat=True)
    exclude_books = list(set(student_books) | set(college_books))
    books_id = [i for i in all_books if i not in exclude_books]
    books = Books.objects.filter(Book_id__in=books_id)
    context = {
        'books':books
    }
    if(request.POST):
        book_id = request.POST.get('optradio')
        if(book_id!=None):
            Book = Books.objects.get(Book_id=book_id)
            i = Request(User=user,Book=Book)
            i.save()
        return redirect('/accounts/student_home')
    return render(request,'../templates/request_book.html',context)
@login_required
def admin_req(request):
    user = request.user
    admin = Admin.objects.filter(user=user).values_list('college',flat=True)
    college = admin[0]
    users = Student.objects.filter(College=college).values_list('user',flat=True)
    books = Request.objects.filter(User__in=users).values_list('Book',flat=True)
    context = {
        'books':books
    }





    return render(request,'../templates/admin_req.html',context)
