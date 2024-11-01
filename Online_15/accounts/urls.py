from django.urls import path
from Online_15.accounts.views import ProfileView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
]