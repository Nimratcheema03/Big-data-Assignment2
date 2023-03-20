# pages/urls.py
from django.urls import path
from .views import homePageView, results, homePost

urlpatterns = [
    path('', homePageView, name='home'),
    path('homePost/', homePost, name='homePost'),
    path('results/<str:concave_points_worst>/<str:perimeter_worst>/<str:concave_points_mean>/<str:radius_worst>/<str:perimeter_mean>/<str:area_worst>/', results, name='results'),
]
