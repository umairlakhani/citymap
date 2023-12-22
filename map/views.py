from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .models import Country, State, APIResponse, City, Town, Address
from .serializers import CountrySerializer, StateSerializer, APIResponseSerializer, CitySerializer, TownSerializer, AddressSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def api_response(**kwargs):
    data = APIResponse(**kwargs)
    serializer = APIResponseSerializer(data)
    return serializer.data

class CountriesView(APIView):
    def get_queryset(self):
        countries = Country.objects.all()
        return countries
    
    def get(self, request, *args, **kwargs):
        serializer = CountrySerializer(self.get_queryset(), many=True)
        return Response(serializer.data)
    
class StatesView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('country_id', in_=openapi.IN_QUERY, description='Either country_id or country_name is required', type=openapi.TYPE_INTEGER),
        openapi.Parameter('country_name', in_=openapi.IN_QUERY, description='Either country_id or country_name is required', type=openapi.TYPE_STRING),
    ])
    def get(self, request, *args, **kwargs):
        country_id = self.request.GET.get('country_id')
        country_name = self.request.GET.get('country_name')
        try:
            if country_id:
                states = State.objects.filter(country__id=country_id)
            elif country_name:
                states = State.objects.filter(country__name__icontains=country_name)
            else:
                return Response(api_response(status="error", data=[], message="Please provide either country_id or country_name as parameters."), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response(api_response(status="error", data=[], message=e), status=status.HTTP_400_BAD_REQUEST)

        serializer = StateSerializer(states, many=True)
        return Response(api_response(status="ok", data=serializer.data, message="success"))
    
class CitiesView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('state_id', in_=openapi.IN_QUERY, description='Either state_id or state_name is required', type=openapi.TYPE_INTEGER),
        openapi.Parameter('state_name', in_=openapi.IN_QUERY, description='Either state_id or state_name is required', type=openapi.TYPE_STRING),
    ])
    def get(self, request, *args, **kwargs):
        state_id = self.request.GET.get('state_id')
        state_name = self.request.GET.get('state_name')
        try:
            if state_id:
                states = City.objects.filter(state_id=state_id)
            elif state_name:
                states = City.objects.filter(state__name__icontains=state_name)
            else:
                return Response(api_response(status="error", data=[], message="Please provide either state_id or state_name as parameters."), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response(api_response(status="error", data=[], message=e), status=status.HTTP_400_BAD_REQUEST)

        serializer = CitySerializer(states, many=True)
        return Response(api_response(status="ok", data=serializer.data, message="success"))
    
class NeighborhoodView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('city_id', in_=openapi.IN_QUERY, description='Either city_id or city_name is required', type=openapi.TYPE_INTEGER),
        openapi.Parameter('city_name', in_=openapi.IN_QUERY, description='Either city_id or city_name is required', type=openapi.TYPE_STRING),
    ])
    def get(self, request, *args, **kwargs):
        city_id = self.request.GET.get('city_id')
        city_name = self.request.GET.get('city_name')
        try:
            if city_id:
                states = Town.objects.filter(city_id=city_id)
            elif city_name:
                states = Town.objects.filter(state__name__icontains=city_name)
            else:
                return Response(api_response(status="error", data=[], message="Please provide either city_id or city_name as parameters."), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response(api_response(status="error", data=[], message=e), status=status.HTTP_400_BAD_REQUEST)

        serializer = TownSerializer(states, many=True)
        return Response(api_response(status="ok", data=serializer.data, message="success"))
    
class StreetView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('city_id', in_=openapi.IN_QUERY, description='Either city_id or city_name is required', type=openapi.TYPE_INTEGER),
        openapi.Parameter('city_name', in_=openapi.IN_QUERY, description='Either city_id or city_name is required', type=openapi.TYPE_STRING),
        openapi.Parameter('town_id', in_=openapi.IN_QUERY, description='Either town_id or town_name is required', type=openapi.TYPE_INTEGER),
        openapi.Parameter('town_name', in_=openapi.IN_QUERY, description='Either town_id or town_name is required', type=openapi.TYPE_STRING),
    ])
    def get(self, request, *args, **kwargs):
        town_id = self.request.GET.get('town_id')
        town_name = self.request.GET.get('town_name')
        city_id = self.request.GET.get('city_id')
        city_name = self.request.GET.get('city_name')
        try:
            if town_id:
                states = Address.objects.filter(town_id=town_id)
            elif town_name:
                states = Address.objects.filter(town__name__icontains=town_name)
            elif city_id:
                states = Address.objects.filter(city_id=city_id)
            elif city_name:
                states = Address.objects.filter(city__name__icontains=city_name)
            else:
                return Response(api_response(status="error", data=[], message="Please include any of the following parameters in your request: town_id, town_name, city_id, or city_name."), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response(api_response(status="error", data=[], message=e), status=status.HTTP_400_BAD_REQUEST)

        serializer = AddressSerializer(states, many=True)
        return Response(api_response(status="ok", data=serializer.data, message="success"))