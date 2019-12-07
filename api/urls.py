from django.urls import path
from .views import *


urlpatterns = [
    path("palestra/", PalestraList.as_view()),
    path("palestra/<int:pk>/", PalestraDetail.as_view()),
    path("form/", PalestraList.as_view()),
    path("form/<int:pk>/", PalestraDetail.as_view()),
    #path("users/", UserCreate.as_view(), name="user_create")
]