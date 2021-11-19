from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   path('',views.home,name = 'home'),
   path('products/',views.products,name = 'products'),
   path('customer/<str:pk_test>/', views.customer, name="customer"),
   path('Order_form/<str:pk_test>/', views.createorder, name="createorder"),
   path('updateorder/<str:pk>/', views.updateorder, name="updateorder"),
   path('delete/<str:pk>/', views.deleteorder, name="deleteorder"),
   path('register/',views.registerPage,name = 'registerPage'),
   path('login/',views.loginPage,name = 'loginPage'),
   path('logout/',views.logoutUser,name = 'logout'),
   path('userprofile/',views.userprofile,name = 'userprofile'),
   path('settings/',views.settings,name = 'settings'),

   path('password_reset/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
   name='password_reset'),
   
   path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
   name='password_reset_done'),
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
   name='password_reset_confirm'),

   path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
   name='password_reset_complete'),

]
