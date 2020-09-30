from django.urls import path
from signal_PS import views

app_name = 'signal_PS'

urlpatterns = [
path('<str:name_ps>/', views.views_ps),
path('', views.views_select_ps),

]