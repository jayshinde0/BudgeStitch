from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from django.conf import settings
    
class CustomUser(AbstractUser): #this contains the clients info
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('tailor', 'Tailor'),
    )
    USER_GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    profilepic = models.ImageField(upload_to='profile_pics/', blank=True, null=True,)
    gender = models.CharField(max_length=10, choices=USER_GENDER)
    experience = models.PositiveIntegerField(blank=True,null=True)
    age = models.PositiveIntegerField(blank=True,null=True)
    dob = models.DateField(blank=True,null=True)
    address = models.CharField(max_length=20,blank=True,null=True)
    addzipcode = models.CharField(max_length=10,blank=True,null=True)
    addcity = models.CharField(max_length=15,blank=True,null=True)
    addstate = models.CharField(max_length=15,blank=True,null=True)
    ratings = models.IntegerField(blank=True,null=True,default=0)
    biodis = models.CharField(max_length=255,blank=True,null=True)
    contact = models.CharField(max_length=15,blank=True,null=True)
    def __str__(self):
        return f"{self.username}"
    
    # Adding related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Change the related_name here
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Change the related_name here
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class DressOrder(models.Model):
    STATUS_CHOICES = (
        ('undecided', 'Undecided'),
        ('pending', 'Accepted'),
        ('declined', 'Declined'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    ordtitle = models.CharField(max_length=50,verbose_name="Order Title",default="")
    user = models.CharField(max_length=30, verbose_name='Username')
    useremail = models.EmailField(verbose_name='Client Email',blank=True,null=True)
    usercontact = models.IntegerField(verbose_name='Client Ph.No',blank=True,null=True)
    userfullname = models.CharField(max_length=50,verbose_name='Client Full Name',blank=True,null=True)
    tailor = models.CharField(max_length=30,verbose_name='Tailor Username')
    tailoremail = models.EmailField(verbose_name='Tailor Email',blank=True,null=True)
    tailorcontact = models.IntegerField(verbose_name='Tailor Ph.No',blank=True,null=True)
    tailorfullname = models.CharField(max_length=50,verbose_name='Tailor Full Name',blank=True,null=True)
    body_size = models.CharField(max_length=20, verbose_name="Body Size")
    cloth_type = models.CharField(max_length=30, verbose_name="Cloth Type")
    budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Budget")
    color = models.CharField(max_length=15, verbose_name="Preferred Color")
    design_reference = models.ImageField(upload_to='design_references/', blank=True, null=True, verbose_name="Design Reference Image")
    additional_notes = models.TextField(blank=True, null=True, verbose_name="Additional Notes")
    created_at = models.DateTimeField(auto_now_add=True)
    orderstatus = models.CharField(max_length=10, choices=STATUS_CHOICES, default='undecided', verbose_name="Order Status")
    clientaddress = models.CharField(max_length=20,blank=True,null=True)
    clientaddzipcode = models.CharField(max_length=10,blank=True,null=True)
    clientaddcity = models.CharField(max_length=15,blank=True,null=True)
    clientaddstate = models.CharField(max_length=15,blank=True,null=True)

    deliverydate = models.DateField(blank=True,null=True,verbose_name="Expected Delivery")
    deliverypatner = models.CharField(blank=True,null=True,max_length=50)
    deliveryinfo = models.CharField(blank=True,null=True ,max_length=50)

    def __str__(self):
        return f"{self.ordtitle} - {self.user.username} to {self.tailor}"
