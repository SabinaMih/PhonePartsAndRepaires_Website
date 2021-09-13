from django.urls import path
from . import views
from .views import signupView, signinView, signoutView, UserEditView

app_name='accounts'

urlpatterns = [
    path('create/', signupView, name='signup'),
    path('login/', signinView, name='signin'),
    path('logout/', signoutView, name='signout'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
   
]