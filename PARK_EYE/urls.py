from django.urls import path
from . import views

urlpatterns=[
    path('register/', views.register, name='register'),
    path('complain/',views.complain, name='complain'),
    path('add_suspected_vehicle/',views.add_suspected_vehicle, name='add_suspected_vehicle'),
    path('thanks/',views.thanks, name='thanks'),
    path('policelogin/', views.policelogin, name='policelogin'),
    path('policelogincheck/', views.police_login_check, name='police_login_check'),
    path('policedashboard/', views.policedashboard, name='police_dashboard'),
]