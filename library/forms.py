from django import forms

# this is a form to import all details of an order from the admin

class order_details_form(forms.Form):
    Book_name = forms.CharField(max_length=255)
    Book_id = forms.CharField(max_length=255, required=True)
    Quantity = forms.IntegerField(max_length=255, required=True)
    # not sure if this is needed or not
    Price_points = forms.IntegerField(max_length=255, required=True)
