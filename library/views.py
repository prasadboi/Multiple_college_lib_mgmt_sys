from accounts.models import Admin
from library.forms import order_details_form
from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponse
from datetime import timedelta
from django.utils import timezone
from django.views.generic import CreateView
from .models import Inventory, Payment_bill, Books, Seller, Seller_inventory
from django import forms


# Create your views here.
#-----------------------------------------------------------------------------------------------------------
# function that dispalys all the transactions made in a time period,
# default is previous week
# for now it just prints all the transactions made
# this function automatically adds a row whenever an order is placed
def payment_details(request):
    payments = Payment_bill.objects.order_by('-date')[:100]
    context = {'payments': payments}
    return render(request,'../templates/payment_details.html', context)
#--------------------------------------------------------------------------------------------------------




#--------------------------------------------------------------------------------------------------------
# functions that display the list of sellers who can accomodate the book order 
# and their net prices
def enter_order_specs(request):
    user = request.user
    if request.method == 'POST':
        form = order_details_form(request.POST)
        if form.is_valid():
            # getting details of the values from the form
            request.session['Book_id'] = form.cleaned_data['Book_id']
            request.session['Book_name'] = form.cleaned_data['Book_name']
            request.session['Quantity'] = form.cleaned_data['Quantity']
            request.session['Price_points'] = form.cleaned_data['Price_points']
            #request.session['College_id'] = form.cleaned_data['College_id']

            redirect(request, '../templates/place_order.html')

        else :
            form = order_details_form()
    return render(request,'../templates/enter_order_specs.html', {'form': form})


# place an order
# the idea is that when you place an order it gets auto updated 
# in the Payment_bills database model as well.

def place_order(request):
    user = request.user
    # given the book id and quantity 
    # i am getting all the sellers who can accomodate this order
    available_sellers = Seller_inventory.objects.filter(book__Book_id__exact = request.session['Book_id'], book_count__gte = request.session['Quantity']).order_by('seller__shippingCost')
    context = {'available_sellers' : available_sellers}
    # on the same page we will display a table with buttons 
    # as options to select the sellers who can accomodate the order.
    admin = Admin.objects.get(user = user)
    admin_college = admin.College
    if(request.POST):
        seller_id = request.post.get('seller_opt_radio')
        if(seller_id != None):
            seller = Seller.objects.get(Seller_id= seller_id)
            # need to add the books quantity to the database inventory
            # if the book is already in inventory update its Book_count
            if (Inventory.objects.filter(Books__Book_id__exact= request.session['Book_id'], College= admin_college).exists()):
                already_existing_book = Books.objects.get(Book_id__exact = request.session['Book_id'])
                already_existing_book.Book_count = already_existing_book.Book_count + request.session['Quantity']

                cost_of_purchase = seller.Shipping_cost + (request.session['Quantity']*request.session['Price_points']*35)
                payment = Payment_bill(cost= cost_of_purchase, book= already_existing_book, seller= seller, college= admin_college)
                payment.save()
            # if the book is not in inventory create a new book and set it Book_count
            else:
                new_book = Books(Book_id = request.session['Book_id'], Book_name = request.session['Book_name'], Price_points = request.session['Price_points'])
                new_book.save()
                cost_of_purchase = seller.Shipping_cost + (request.session['Quantity']*request.session['Price_points']*35)
                payment = Payment_bill(cost= cost_of_purchase, book= new_book, seller= seller, college = admin_college)
                payment.save()
        # redirecting to the admin home url
        return redirect('/library/admin_home')
        
    return render(request, '../templates/place_order.html', context)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



