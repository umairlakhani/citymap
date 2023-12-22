# appname/urls.py
from django.urls import path
from .views import CountriesView, StatesView, CitiesView, NeighborhoodView, StreetView

urlpatterns = [
    path('countries', CountriesView.as_view()),
    path('states', StatesView.as_view(), name='state-list'),
    path('cities', CitiesView.as_view(), name='city-list'),
    path('neighborhoods', NeighborhoodView.as_view(), name='neighborhood-list'),
    path('streets', StreetView.as_view(), name='street-list'),
]