from django.urls import path
from .import views
urlpatterns=[
    path('',views.Signup,name='Signup'),
    path('home',views.Home,name='Home'),
    path('signin',views.Signin,name='Signin'),
    path('text',views.Text,name="Text"),
    path('image',views.Image,name="Image"),
    path('signout',views.Signout,name='Signout'),
    path('contact',views.Contactus,name="Contactus"),
    path('ddelete/<str:prompt>/',views.Ddelete,name="Ddelete"),
    path('idelete/<str:msg>/',views.Idelete,name="Idelete"),
]