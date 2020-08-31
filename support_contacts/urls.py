from django.urls import path
from support_contacts import views

app_name = 'support_contacts'

urlpatterns = [
path('', views.contacts),
]