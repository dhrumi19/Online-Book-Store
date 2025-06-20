from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
