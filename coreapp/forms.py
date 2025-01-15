from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm,PasswordChangeForm
from .models import CustomUser,DressOrder  # Make sure to import your custom user model

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('Null','Choose UserType'),
        ('client', 'Client'),
        ('tailor', 'Tailor'),
    ]
    USER_GENDER = (
        ('null','Choose Gender'),
        ('other','Other'),
        ('male', 'Male'),
        ('female', 'Female'),
    )
    username = forms.CharField(
        max_length=10,
        label='Username',
        error_messages={
            'required':'You must have a Username to open an account'
        },
        widget= forms.TextInput(attrs={'class': 'form-control custom-bg text-dark'})
    )
    password1 = forms.CharField(
        max_length=10,label='Password',
        widget=forms.PasswordInput(attrs={'class':'form-control custom-bg text-dark'})
        
        )
    password2 = forms.CharField(max_length=10,label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control custom-bg text-dark'}))
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True, label="User Type",widget=forms.Select(attrs={'id':'usertype','class':'form-select custom-bg text-dark','onchange':'toggleExperienceField()'}))
    gender = forms.ChoiceField(choices=USER_GENDER, required=True, label="User Gender",widget=forms.Select(attrs={'class':'form-select custom-bg text-dark'}))  # Change CharField to ChoiceField
    experience = forms.IntegerField(max_value=99, required=False,widget=forms.NumberInput(attrs={'id':'usertype','class':'form-control custom-bg text-dark'}))  # Add required=False if not mandatory
    age = forms.IntegerField(max_value=150, min_value=15, required=True,widget=forms.NumberInput(attrs={'class':'form-control custom-bg text-dark'}))  # Make sure to specify required
    dob = forms.DateField(required=True, label="Date of Birth",widget=forms.DateInput(attrs={'type':'date','class':'form-control custom-bg text-dark'}))  # Adding label for clarity
    profilepic = forms.ImageField(required=False,label="Profile Image",widget=forms.FileInput(attrs={'class':'form-control custom-bg text-dark'}))
    address = forms.CharField(max_length=30,label='Address (House or Road Name)',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    addzipcode = forms.CharField(max_length=30,label='Zipcode',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    addcity = forms.CharField(max_length=30,label='City Name',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    addstate = forms.CharField(max_length=30,label='State Name',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    email = forms.EmailField(required=True,label='Email',widget=forms.EmailInput(attrs={'class':'form-control custom-bg text-dark','type':'email'}))
    first_name = forms.CharField(required=True,label='First Name',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    last_name = forms.CharField(required=True,label='Last Name',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    contact = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={'class':'form-control custom-bg text-dark'}))
    class Meta:
        model = CustomUser
        fields = ('username','first_name','last_name','email', 'password1', 'password2','contact', 'user_type', 'gender','profilepic', 'experience','address','addzipcode','addcity','addstate', 'age', 'dob') 

class DressOrderForm(forms.ModelForm):
    clientaddress = forms.CharField(max_length=30,label='Address (House or Road Name)',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}),error_messages={'required':'Address cannot be empty.'})
    clientaddzipcode = forms.CharField(max_length=30,label='Zipcode',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}),error_messages={'required':'Zipcode cannot be empty.'})
    clientaddcity = forms.CharField(max_length=30,label='City Name',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}),error_messages={'required':'City cannot be empty.'})
    clientaddstate = forms.CharField(max_length=30,label='State Name',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}),error_messages={'required':'State cannot be empty.'})
    class Meta:
        model = DressOrder
        fields = ['ordtitle', 'body_size', 'cloth_type', 'budget', 'color', 'deliverydate','design_reference', 'additional_notes','clientaddress','clientaddzipcode','clientaddcity','clientaddstate']
        widgets = {
            'design_reference': forms.ClearableFileInput(attrs={'multiple': False,'class':'form-control custom-bg  text-dark'}),
            'ordtitle': forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}),
            'body_size': forms.TextInput(attrs={'class':'form-control custom-bg text-dark','placeholder':'chest-waist-hip-bodyheight'}),
            'cloth_type': forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}),
            'budget': forms.NumberInput(attrs={'class':'form-control custom-bg text-dark'}),
            'color': forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}),
            'additional_notes': forms.Textarea(attrs={'class':'form-control custom-bg text-dark'}),
            'deliverydate': forms.DateInput(attrs={'type':'date','class':'form-control custom-bg text-dark'})
        }

class DressStatusForm(forms.ModelForm):
    class Meta:
        model = DressOrder
        fields = ['body_size', 'cloth_type', 'budget', 'color', 'design_reference', 'additional_notes','orderstatus']
        widgets = {
            'design_reference': forms.ClearableFileInput(attrs={'multiple': False}),
        }

class CustomAuthForm(AuthenticationForm):

    username = forms.CharField(max_length=20,label="Username",widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    password = forms.CharField(max_length=10,label='Password',widget=forms.PasswordInput(attrs={'class':'form-control custom-bg text-dark'}))
    class Meta:
        model = AuthenticationForm
        fields = ['username','password']

class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(required=True,label='First Name',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    last_name = forms.CharField(required=True,label='Last Name',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    email = forms.EmailField(required=True,label='Email',widget=forms.EmailInput(attrs={'class':'form-control custom-bg text-dark','type':'email'}))
    profilepic = forms.ImageField(required=False,label="Profile Image",widget=forms.FileInput(attrs={'class':'form-control custom-bg text-dark'}))
    contact = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={'class':'form-control custom-bg text-dark'}))
    address = forms.CharField(required=True,label='Address',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    addzipcode = forms.CharField(required=True,label='Zip Code',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    addcity = forms.CharField(required=True,label='City Name',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    addstate = forms.CharField(required=True,label='State Name',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    biodis = forms.CharField(max_length=255,label='Bio',widget=forms.Textarea(attrs={'class':'form-control custom-bg text-dark','placeholder':'keep it short and concise, mention your speciality'}))
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','email','profilepic','biodis','contact','address','addzipcode','addcity','addstate')

class ChangeAddressForm(UserChangeForm):
    address = forms.CharField(required=True,label='Address',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    addzipcode = forms.CharField(required=True,label='Zip Code',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    addcity = forms.CharField(required=True,label='City Name',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    addstate = forms.CharField(required=True,label='State Name',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark'}))
    class Meta:
        model = CustomUser
        fields = ('address','addzipcode','addcity','addstate')

class DeliverOrderForm(forms.ModelForm):
    deliverypatner = forms.CharField(required=True,label='Delivery Patner:',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark','placeholder':'Name and Contact of Delivery Patner'}))
    deliveryinfo = forms.CharField(required=True,label='Delivery Info:',widget=forms.TextInput(attrs={'class':'form-control custom-bg text-dark','placeholder':'Tracking Id'}))
    class Meta:
        model = DressOrder
        fields = ('deliverypatner','deliveryinfo')