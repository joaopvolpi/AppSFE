from django.urls import path
from .views import *


urlpatterns = [
    path("palestra/", PalestraList.as_view(), name="PalestraList"),
    path("palestra/<int:pk>/", PalestraDetail.as_view(), name="PalestraDetail")
]