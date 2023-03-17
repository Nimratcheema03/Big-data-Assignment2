# pages/urls.py
from django.urls import path
from .views import homePageView, results, homePost

urlpatterns = [
    path('', homePageView, name='home'),
    path('homePost/', homePost, name='homePost'),
    path('results/<int:Rank>/<str:NA_Sales>/<str:EU_Sales>/<str:JP_Sales>/<str:Other_Sales>/', results, name='results'),

]
