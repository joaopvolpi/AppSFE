from django.urls import path
from .views import *


urlpatterns = [
    path("palestra/", PalestraList.as_view()),
    path("palestra/<int:pk>/", PalestraDetail.as_view()),
    path("form/", FormList.as_view()),                             #VER LISTA DE FORMS - ADMIN
    path("form/<int:pk>/", FormDetail.as_view()),
    path("users/", UserList.as_view()),                            #VER DETERMINADO USUARIO
    path("users/<int:pk>/", UserDetail.as_view()),                 #VER LISTA DE USUARIOS  -ADMIN
    path("login/", LoginView.as_view(), name="login"),             #FAZER LOGIN (método post)
    path("createusers/", UserCreate.as_view(), name="user_create") #CRIA OS USUARIOS  -ADMIN
]