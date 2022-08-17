from django.db import models
from django.conf import settings
 #Create your models here.

 # COLLEGE-------------------------------------------------------------------------------------------------------------------------------------
class College(models.Model):
    College_id = models.CharField(primary_key=True,max_length=255)
    College_name = models.CharField(max_length=255,null=True)
    College_population = models.IntegerField(null=True)
    city = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255,null=True)
    pincode = models.IntegerField(null=True)
    Director = models.CharField(max_length=255,null=True)
#----------------------------------------------------------------------------------------------------------------------------------------




# BOOKS--------------------------------------------------------------------------------------------------------------------------------
class Books(models.Model):
    Book_id = models.CharField(primary_key=True,max_length=255)
    Book_name = models.CharField(max_length=255)
    Publisher = models.CharField(max_length=255)
    Author = models.CharField(max_length=255)
    Book_type = models.CharField(max_length=255)
    Price_points = models.CharField(max_length=255)
#--------------------------------------------------------------------------------------------------------------------------------------




# INVENTORY----------------------------------------------------------------------------------------------------------------------------
class Inventory(models.Model):
    College = models.ForeignKey(College,on_delete=models.CASCADE)
    Books = models.ForeignKey(Books,on_delete=models.CASCADE)
    Book_count = models.IntegerField(default=0)
#---------------------------------------------------------------------------------------------------------------------------------------




# SELLER--------------------------------------------------------------------------------------------------------------
class Seller(models.Model):
    # seller's name
    Seller_name = models.CharField(max_length=255, null= False)
    Seller_id = models.CharField(primary_key=True, max_length=255)
    Shipping_cost = models.IntegerField(max_length=255, null= True )
    Rating = models.IntegerField(null=False)
    # address details of seller
    pincode = models.IntegerField(null=True)
    city = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255,null=True)
    # seller's account number
    Account_no = models.CharField(max_length=255, null = False, unique = True)
#------------------------------------------------------------------------------------------------------------------




# TRANSACTION--------------------------------------------------------------------------------------------------------
class Payment_bill(models.Model):
    college = models.ForeignKey(College,on_delete=models.CASCADE)
    time_of_transaction = models.DateTimeField(auto_now_add= True)
    cost = models.IntegerField(max_length=255, null = False)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
#-------------------------------------------------------------------------------------------------------------------



# SELLER INVENTORY------------------------------------------------------------------------------------------------------------------
class Seller_inventory(models.Model):
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    book_count = models.IntegerField(max_length=255, null=True)
#----------------------------------------------------------------------------------------------------------------------

