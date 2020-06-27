from django.urls import path
from website import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='word search'),
    path('details/', views.details, name='word details')
]