from django.urls import path
from .import views
from django.conf.urls import url

urlpatterns = [
    path('', views.home_page, name="home"),
    path('prices/', views.prices, name="prices"),
    path('allavailablecoins/', views.allCoin, name="allavailablecoins"),
    path('search_auto/', views.search_auto, name="search_auto"),
]
