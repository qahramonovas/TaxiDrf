from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from management.models import Station, User
from management.serializer import StationSerializer, RegisterModelSerializer

@extend_schema(tags=['Auth'],)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass
@extend_schema(tags=['Auth'],)
class CustomTokenRefreshView(TokenRefreshView):
    pass



@extend_schema(tags=['Auth'],)
class RegisterAPIView(CreateAPIView):
   serializer_class = RegisterModelSerializer
   queryset = User.objects.all()




@extend_schema(tags=['Station'],)
class StationListView(ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


@extend_schema(tags=['Station'],)
class StationDetailView(RetrieveAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    lookup_field = 'id'


@extend_schema(tags=['Station'],)
class StationByRegionView(ListAPIView):
    serializer_class = StationSerializer
    def get_queryset(self):
        region_id = self.kwargs['regionID']
        return Station.objects.filter(region_id=region_id)