from .views import Agency,SocialSecurity,Code,home
from django.urls import path,include

urlpatterns = [
  
    path('virtual', Agency, name="virtual"),
    path('SocialSecurity', SocialSecurity,name="SocialSecurity"),
    path('Code', Code, name="Code"),
    path('home', home, name="home"),
]
