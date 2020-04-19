from django.urls import path
from .import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('prices/', views.prices, name="prices"),
    path('allavailablecoins/', views.allCoin, name="allavailablecoins"),
]