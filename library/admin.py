from django.contrib import admin

# Register your models here.
from .models import College, Books, Inventory, Seller, Payment_bill, Seller_inventory

admin.site.register(College)
admin.site.register(Books)
admin.site.register(Inventory)
admin.site.register(Seller)
admin.site.register(Payment_bill)
admin.site.register(Seller_inventory)