from django.urls import path
from .views import *


urlpatterns = [
    path("palestra/", PalestraList.as_view()),
    path("palestra/<int:pk>/", PalestraDetail.as_view()),
    path("form/", FormList.as_view()),
    path("form/<int:pk>/", FormDetail.as_view()),
    path("users/", UserList.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),
    #path("users/", UserCreate.as_view(), name="user_create")
]