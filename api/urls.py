from django.urls import path
from .views import *
from api import views
from django.views.generic import TemplateView

from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='API')

#from rest_framework.schemas import get_schema_view

urlpatterns = [
    path("palestra/", PalestraList.as_view()),
    path("palestra/<int:pk>/", PalestraDetail.as_view()),
    path("palestra/post/", PalestraPost.as_view()),
    path("palestra/delete/<int:pk>/", PalestraDelete.as_view()),
    path("palestra/update/<int:pk>/", PalestraEdit.as_view()),

    path("form/", FormList.as_view()),                             #VER LISTA DE FORMS - ADMIN
    path("form/<int:pk>/", FormDetail.as_view()),

    path("users/", UserList.as_view()),                            #VER LISTA DE USUARIOS  -ADMIN
    path("users/<int:pk>/", UserDetail.as_view()),                 #VER DETERMINADO USUARIO
    path("login/", LoginView.as_view(), name="Login"),             #FAZER LOGIN (método post)
    #path("logout/", LogoutView.as_view(), name="login"),
    path("createusers/", UserCreate.as_view(), name="user_create"), #CRIA OS USUARIOS  -ADMIN

    path("addfotoperfil/", AddFotoPerfilView.as_view()), 
    path("favoritar/<int:id>/", FavoriteView().as_view(), name="favoritar"),  
    path("verfavoritos/", ListaFavs.as_view(), name="lista_favoritos"),


    #Essas URLs abaixo são apenas para documentar

    path("swagger/", schema_view), 


]

'''
path('swagger-ui/', TemplateView.as_view(
template_name='swagger-ui.html',
extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),

path('openapi/', get_schema_view(
    title="API AppSFE",
    description="La semaine Fluxo",
    version="1.0.0"
), name='openapi-schema'),
'''

