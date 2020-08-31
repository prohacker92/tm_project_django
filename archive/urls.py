from django.urls import path,re_path
from archive import views

app_name = 'archive'

urlpatterns = [
path('', views.show_archive),
]