from rest_framework.serializers import ModelSerializer

from apps.models import Region
from management.models import Station
from management.models import User


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'birth_date' ,'gender' ,'prava', 'phone_number' , 'password' ]




class RegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']

class StationSerializer(ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = Station
        fields = ['id', 'name', 'latitude', 'longitude', 'region']