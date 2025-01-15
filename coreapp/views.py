from django.shortcuts import render,HttpResponseRedirect,get_object_or_404,get_list_or_404,redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import CustomUserCreationForm,DressOrderForm,CustomAuthForm,CustomUserChangeForm,ChangeAddressForm,PasswordChangeForm,DeliverOrderForm
from .models import CustomUser,DressOrder
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
# Create your views here.
def landingpage(request):
    return render(request,'index.html')

def aboutus(request):
    return render(request,'aboutus.html')

def profile(request):
    orders = DressOrder.objects.filter(user=request.user.username).order_by('-created_at')
    return render(request,'profile.html',{'orders':orders})


def usersignup(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Please Logout Before Signing up New account')
        return HttpResponseRedirect('/userprofile')
    
    if request.method == 'POST':
        fm = CustomUserCreationForm(request.POST,request.FILES)
        if fm.is_valid():
            user = fm.save(commit=False)  # Get user instance without saving
            user.user_type = fm.cleaned_data['user_type']  # Set user_type
            user.gender = fm.cleaned_data['gender']
            user.experience = fm.cleaned_data['experience']
            user.age = fm.cleaned_data['age']
            user.dob = fm.cleaned_data['dob']
            user.save()  # Save user instance with the selected role
            messages.success(request, 'Congrats, You have created your account!!')
            return HttpResponseRedirect('/userlogin')
    else:
        fm = CustomUserCreationForm()
    
    return render(request, 'usersignup.html', {'form': fm})



def userlogin(request):
    if request.user.is_authenticated:
        messages.warning(request,'Please Logout this accout to login')
        return HttpResponseRedirect('/profile')
    if request.method == 'POST':
        fm = CustomAuthForm(request=request,data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                messages.success(request,'You have Logged In Successfully!!')
                return HttpResponseRedirect('/userprofile')
    else:
        fm = CustomAuthForm()
    return render(request,'userlogin.html',{'form':fm})

@login_required
def userlogout(request):
    logout(request)
    messages.info(request,'You hava Logged Out Successfully')
    return HttpResponseRedirect('/userlogin/')

@login_required
def order(request):

    #handles the filter (get) request
    filter_type = request.GET.get('filter','default')
    if filter_type:
        if filter_type == 'top_rated':
            tailors = CustomUser.objects.filter(user_type='tailor')
        elif filter_type == 'near_me':
            tailors = CustomUser.objects.filter(user_type='tailor',addcity=request.user.addcity)
        elif filter_type == 'default':
            tailors = CustomUser.objects.filter(user_type='tailor')
    
    #handles the search (get) request
    search_query = request.GET.get('search','')
    if search_query:
        tailors = CustomUser.objects.filter(username__startswith=search_query,user_type='tailor')

    #handles the displaying of the tailors cards
    paginator = Paginator(tailors, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'order.html', {'tailors': page_obj})

@login_required
def placeorder(request, id):
    if request.user.is_authenticated:
        if request.user.user_type == 'tailor':
            messages.info(request, 'Only Clients and place Orders')
            return HttpResponseRedirect('/userprofile/') 
        tailordetail = get_object_or_404(CustomUser, id=id, user_type='tailor')
        if request.method == 'POST':
            form = DressOrderForm(request.POST, request.FILES)
            if form.is_valid():
                dress_order = form.save(commit=False)
                dress_order.user = request.user.username
                dress_order.useremail = request.user.email
                dress_order.usercontact = request.user.contact
                dress_order.userfullname = f"{request.user.first_name} {request.user.last_name}".strip()
                dress_order.tailor = tailordetail.username
                dress_order.tailoremail = tailordetail.email
                dress_order.tailorcontact = tailordetail.contact
                dress_order.tailorfullname =  f"{tailordetail.first_name} {tailordetail.last_name}".strip()
                dress_order.save()
                messages.info(request, 'You have placed the order successfully.')
                return HttpResponseRedirect('/userprofile/')
        else:
            form = DressOrderForm()
    else:
        messages.info(request, 'Please Login to Place Order')
        return HttpResponseRedirect('/userlogin/') 
    
    return render(request, 'placeorder.html', {'form': form, 'tailordetail': tailordetail})

@login_required
def manageorder(request,id):
    orderdetail = get_object_or_404(DressOrder,id=id)
    return render(request,'manageorder.html',{'order':orderdetail})

@login_required
def orderstatus(request,id,status):
    obj = get_object_or_404(DressOrder, id=id)
    if status.lower() == 'true':
        obj.orderstatus = 'pending'  # Assuming you have a status field with values like 'accepted' or 'rejected'
        obj.save()
        messages.success(request, 'Order Accepted')
        return HttpResponseRedirect('/tailor_dashboard/')
    elif status.lower() == 'false':
        obj.orderstatus = 'Declined'
        obj.save()
        messages.info(request, 'Order Declined')
        return HttpResponseRedirect('/tailor_dashboard/')
    elif status.lower() == 'comp':
        obj.orderstatus = 'Completed'
        obj.save()
        messages.success(request, 'Order Completed')
        return HttpResponseRedirect('/tailor_dashboard/')
    else:
        messages.info(request, 'Select Valid Option.')
        return HttpResponseRedirect('/tailor_dashboard/')

@login_required
def trackorder(request):
    pass

@login_required
def vieworders(request):
    if request.user.user_type == 'tailor':
        name = request.user.username
        orders = DressOrder.objects.filter(tailor=name).order_by('-created_at')
        neword = DressOrder.objects.filter(tailor=name,orderstatus='undecided').count()
        pendord = DressOrder.objects.filter(tailor=name,orderstatus='pending').count()
    else:
        return redirect('/userprofile/')
    return render(request,'tailor_dashboard.html',{'orders':orders,'neword':neword,'pendord':pendord})

@login_required
def uservieweditorder(request,id):
    orderdetail = get_object_or_404(DressOrder,id=id)
    return render(request,'vieweditorder.html',{'order':orderdetail})

@login_required
def viewprofile(request,id):
    prof = CustomUser.objects.get(id=id)
    return render(request,'viewprofile.html',{'x':prof})

@login_required
def editinfo(request):
    if request.method == "POST":
        fm = CustomUserChangeForm(request.POST,request.FILES,instance=request.user )
        if fm.is_valid():
            fm.save()
            messages.success(request,'Profile Edited Successfully!!')
            return HttpResponseRedirect('/userprofile')
    else:
        fm = CustomUserChangeForm(instance=request.user)
    return render(request,'userinfochange.html',{'form':fm})

@login_required
def changepass(request):
    if request.method == 'POST':
        fm = PasswordChangeForm(user=request.user,data=request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Password Updated Successfully!!')
            return HttpResponseRedirect('/userlogin')
        
    else:
        fm = PasswordChangeForm(user=request.user)
    return render(request,'changepass.html',{'form':fm})