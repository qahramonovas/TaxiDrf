# from django.contrib import admin
from django.urls import path

from management.views import CustomTokenObtainPairView, CustomTokenRefreshView, RegisterAPIView, StationListView, \
    StationDetailView, StationByRegionView

urlpatterns = [
    path('api/v1/station/', StationListView.as_view(), name='station-list'),
    path('api/v1/station/<int:id>/', StationDetailView.as_view(), name='station-detail'),
    path('api/v1/station/<int:regionID>/', StationByRegionView.as_view(), name='station-by-region'),
]


urlpatterns += [
    path('auth/token/', CustomTokenObtainPairView.as_view()),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view()),
    path('register/', RegisterAPIView.as_view())
]






