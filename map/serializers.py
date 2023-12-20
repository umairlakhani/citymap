from rest_framework import serializers
from .models import Country, State, APIResponse, Town, City, Address

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
        
class StateSerializer(serializers.ModelSerializer):
    # country = CountrySerializer(read_only=True)
    class Meta:
        model = State
        fields = '__all__'
        
class CitySerializer(serializers.ModelSerializer):
    # country = CountrySerializer(read_only=True)
    class Meta:
        model = City
        fields = '__all__'
        
class TownSerializer(serializers.ModelSerializer):
    # country = CountrySerializer(read_only=True)
    class Meta:
        model = Town
        fields = '__all__'
        
class AddressSerializer(serializers.ModelSerializer):
    # country = CountrySerializer(read_only=True)
    class Meta:
        model = Address
        fields = '__all__'
        
class APIResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIResponse
        # fields = "__all__"
        exclude = ('id',)
