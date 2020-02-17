from django.urls import path
from .views import *
from api import views
from django.views.generic import TemplateView

from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='API')

#from rest_framework.schemas import get_schema_view

urlpatterns = [
    path("palestra/", PalestraList.as_view()),
    path("p/<str:date>", PalPorDia.as_view()), #PALESTRA POR DIA, ORDENADO POR HORA

    path("palestra/<int:pk>/", PalestraDetail.as_view()),
    path("palestra/post/", PalestraPost.as_view()),
    path("palestra/delete/<int:pk>/", PalestraDelete.as_view()),
    path("palestra/update/<int:pk>/", PalestraEdit.as_view()),

    path("form/<int:id>/", FormPost.as_view()),                #USUARIO AVALIA A PALESTRA QUE VISITOU
    

    path("users/", UserList.as_view()),                            #VER LISTA DE USUARIOS  -ADMIN
    path("users/<int:pk>/", UserDetail.as_view()),                 #VER DETERMINADO USUARIO
    path("login/", LoginView.as_view(), name="Login"),             #FAZER LOGIN (método post)
    #path("logout/", LogoutView.as_view(), name="login"),
    path("createusers/", UserCreate.as_view(), name="user_create"), #CRIA OS USUARIOS  -ADMIN

    path("addfotoperfil/", AddFotoPerfilView.as_view()), 
    path("favoritar/<int:id>/", FavoriteView().as_view(), name="favoritar"),  
    path("verfavoritos/", ListaFavs.as_view(), name="lista_favoritos"),

    path("validar/<int:id>/", ValidacaoView.as_view()), #ESSE EH O TESTE DO QR CODE SEM QR CODE

    path("foinapalestra/<int:id>/", FoiNaPalestraList.as_view()), 



    #Essa URL abaixo são apenas para documentar, apesar de não estar funcionando direito

    path("swagger/", schema_view), 


]



