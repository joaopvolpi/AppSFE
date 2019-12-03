from django.urls import path
from .views import *


urlpatterns = [
    path("palestra/", PalestraList.as_view()),
    path("palestra/<int:pk>/", PalestraDetail.as_view())
]