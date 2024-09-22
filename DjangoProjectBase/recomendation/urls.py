from django.urls import path 
from . import views 

urlpatterns = [ 
    path('', views.recomendation, name='recomendation'), 
]

