from django.urls import path, include
from .views import *
from api import views
from django.conf import settings
from django.conf.urls.static import static 
from rest_framework import permissions

urlpatterns = [

    path("palestra/", PalestraList.as_view()),
    path("p/<str:date>/", PalPorDia.as_view()), #PALESTRA POR DIA, ORDENADO POR HORA

    path("palestra/<int:pk>/", PalestraDetail.as_view()),
    path("palestra/post/", PalestraPost.as_view()),
    path("palestra/delete/<int:pk>/", PalestraDelete.as_view()),


    path("users/", UserList.as_view()),                            #VER LISTA DE USUARIOS  -ADMIN
    path("login/", LoginView.as_view(), name="Login"),             #FAZER LOGIN (método post)
    path("loginadmin/", LoginAdminView.as_view()),             #FAZER LOGIN ADMIN NO SW(método post)
    path("logout/", LogoutView.as_view(), name="logout"),           #FAZER LOGOUT (método get)
    path("createusers/", UserCreate.as_view(), name="user_create"), #CRIA OS USUARIOS  -ADMIN

    path("favoritar/<int:id>/", FavoriteView().as_view(), name="favoritar"),  
    path("verfavoritos/", ListaFavs.as_view(), name="lista_favoritos"),

    path("validar/<int:id>/", ValidacaoView.as_view()), #ESSE EH O TESTE DO QR CODE SEM QR CODE

    path("foinapalestra/<int:id>/", FoiNaPalestraList.as_view()), 

    path("parceiros/", ParceirosGet.as_view()),

    path("parceiros/post/", ParceiroPost.as_view()),

    path("parceiros/delete/<int:pk>/", ParceiroDelete.as_view()),


    path("cores/post/", CriarObjetoCor.as_view()), #NÃO DEVE SER ACESSADO NUNCA
    path("cores/edit/", CorPut.as_view()),
    path("cores/", GetCor.as_view()),

    path("dias/post/", CriarObjetoDia.as_view()), #NÃO DEVE SER ACESSADO NUNCA
    path("dias/edit/", DiasPut.as_view()),
    path("dias/", GetDias.as_view()),

    path("deletageral/", DeleteGeral.as_view()),                   #DELETA GERAL         

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



