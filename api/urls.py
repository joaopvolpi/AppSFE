from django.urls import path, include
from .views import *
from api import views
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static 


from rest_framework import permissions
'''
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Doc AppSFE",
        default_version='v1',
        description="Test description",
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)
'''

urlpatterns = [

    path("palestra/", PalestraList.as_view()),
    path("p/<str:date>/", PalPorDia.as_view()), #PALESTRA POR DIA, ORDENADO POR HORA

    path("palestra/<int:pk>/", PalestraDetail.as_view()),
    path("palestra/post/", PalestraPost.as_view()),
    path("palestra/delete/<int:pk>/", PalestraDelete.as_view()),
    path("palestra/update/<int:pk>/", PalestraEdit.as_view()),

    path("form/<int:id>/", FormPost.as_view()),                             #USUARIO AVALIA A PALESTRA QUE VISITOU
    path("verforms/<int:id>/", VerRespostasForms.as_view()),        #ADMIN VE RESPOSTAS AOS FORMS
    
    

    path("users/", UserList.as_view()),                            #VER LISTA DE USUARIOS  -ADMIN
    path("users/<int:pk>/", UserDetail.as_view()),                 #VER DETERMINADO USUARIO
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

    #path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    #path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



