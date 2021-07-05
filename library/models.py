from django.db import models

 #Create your models here.
class College(models.Model):
    College_id = models.CharField(primary_key=True,max_length=255)
    College_name = models.CharField(max_length=255,null=True)
    College_population = models.IntegerField(null=True)
    city = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255,null=True)
    pincode = models.IntegerField(null=True)
    Director = models.CharField(max_length=255,null=True)

class Books(models.Model):
    Book_id = models.CharField(primary_key=True,max_length=255)
    Book_name = models.CharField(max_length=255)
    Publisher = models.CharField(max_length=255)
    Author = models.CharField(max_length=255)
    Book_type = models.CharField(max_length=255)
    Price_points = models.CharField(max_length=255)

class Inventory(models.Model):
    College = models.ForeignKey(College,on_delete=models.CASCADE)
    Books = models.ForeignKey(Books,on_delete=models.CASCADE)
    Book_count = models.IntegerField(default=0)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['College','Books'],name='College_book_cons')
        ]
