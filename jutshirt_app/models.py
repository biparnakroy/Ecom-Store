from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

#=========== User Model ===========
class CustomUser(AbstractUser):
    user_type_data=((1,"Admin"),(2,"Customer"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

class Admin(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    admin_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    profile_pic = models.FileField(default="/media/user.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Customer(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    customer_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer_year =models.CharField(max_length=100, blank=True)
    customer_phone = models.CharField(max_length=100, blank=True)
    cart= models.CharField(max_length=10000, blank=True)
    discount = models.CharField(max_length=100, blank=True)
    profile_pic = models.FileField(default="/media/user.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#products model

class Products(models.Model):
    uuid=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name= models.CharField(max_length=100, blank=True)
    product_type = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    picture =  models.CharField(max_length=100, blank=True)
    price = models.CharField(max_length=100, blank=True)


#order model
class Order(models.Model):
    uuid=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    oder_customer = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True)
    product_list = models.CharField(max_length=10000, blank=True)
    quantity_list = models.CharField(max_length=10000, blank=True)
    size_list = models.CharField(max_length=10000, blank=True)
    amount = models.CharField(max_length=100, blank=True)
    payment_mode = models.CharField(max_length=100, blank=True)
    is_paid = models.BooleanField()
    is_delivered = models.BooleanField()


#============= Creating signals ============
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            Admin.objects.create(user=instance)
        if instance.user_type==2:
            Customer.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.customer.save()