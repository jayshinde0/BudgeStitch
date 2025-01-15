
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.landingpage,name="Home Page"),
    path('aboutus/',views.aboutus),
    path('userprofile/',views.profile),
    path('usersignup/',views.usersignup),
    path('userlogin/',views.userlogin),
    path('userlogout/',views.userlogout),
    path('viewprofile/<int:id>',views.viewprofile),
    path('edituserinfo/',views.editinfo),
    path('changepass/',views.changepass),

    path('order/',views.order),#order page for client
    path('placeorder/<int:id>',views.placeorder),#client to place the order
    path('trackorder/',views.trackorder), #client to track the order
    path('vieweditorder/<int:id>',views.uservieweditorder),#client can view his order

    path('tailor_dashboard/',views.vieworders),#displays all the orders for tailor
    path('manageorder/<int:id>',views.manageorder),#tailor to manage the order
    path('orderstatus/<int:id>/<str:status>',views.orderstatus)#tailor can accept or reject the order
]