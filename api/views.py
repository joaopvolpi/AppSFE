from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.permissions import * 
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from rest_framework.renderers import TemplateHTMLRenderer

from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()

#from rest_framework_swagger.views import get_swagger_view
#schema_view = get_swagger_view(title='API')


'''

-Ajeitar o serializer para o favorito da palestra retornar True ou False quando
requisitado por determinado usuário, e não o favorito mostrar a lista de usuários
que favoritaram a palestra. 


'''
      
class FavoriteView(APIView):
    def get(self, request, id):
        palestra = get_object_or_404(Palestra, id=id)

        print(palestra)
        print(request.user) #Está retornando AnonymousUser ERRADO // Ta mais não :D
        print(request.user.is_authenticated)
        print(request.user.id)

        if palestra.favorito.filter(id=request.user.id).exists():
            palestra.favorito.remove(request.user)
            return Response(data={ "message": "Palestra removida dos favoritos" }, status=status.HTTP_200_OK)
        else:
            palestra.favorito.add(request.user)
            return Response(data={ "message": "Palestra favoritada" }, status=status.HTTP_200_OK)
     

class ListaFavs(APIView):   #View que mostra a lista de favoritos do usuário
    def get(self, request):
        user = request.user
        lista_favs = user.favorito.all()            
        data = PalestraSerializer(lista_favs, many=True).data
        return Response(data)


class PalestraList(APIView):
    def get(self, request):
        palestra = Palestra.objects.all().order_by('inicio')
        data = PalestraSerializer(palestra, many=True).data   #VIEW P/ VER LISTA DE PALESTRAS
        
        return Response(data)


class PalestraDetail(APIView):
    def get(self, request, pk):
        palestra = get_object_or_404(Palestra, pk=pk)     #VIEW P/ VER PALESTRA PARTICULAR
        '''
        if palestra.favorito.filter(id=request.user.id).exists():
            fav_user = True
        else:
            fav_user = False

        serializer = PalestraSerializer(palestra, context={'fav_user': fav_user})
        
        '''
        serializer = PalestraSerializer(palestra, context={'request': request})
        print(request.query_params)
        return Response(serializer.data)


class PalestraPost(APIView):

    permission_classes  = [IsAdminUser]  

    '''

    View para postar palestra (separei das outras pq eh necessario ser admin para postar, assim como 
    para deletar e editar as palestras). Como não consegui uma maneira fácil de separar os métodos
    por permissões, separei as views. 


    '''

    def post(self, request):
        tema = request.data['tema']
        descricao_palestra = request.data['descricaopalestra']
        palestrante = request.data['palestrante']
        descricao_palestrante = request.data['descricaopalestrante']
        sala = request.data['sala']
        inicio = request.data['inicio']
        termino = request.data['termino']
        data = request.data['dia']
        fotopalestrante = request.data['fotopalestrante']

        postagem = Palestra(tema= tema, termino=termino, descricaopalestra=descricao_palestra, palestrante=palestrante, descricaopalestrante=descricao_palestrante, sala=sala, inicio=inicio, dia=data, fotopalestrante=fotopalestrante)
        postagem.save()
        data = PalestraSerializer(postagem).data
        return Response(data)


class PalestraDelete(APIView):

    permission_classes  = [IsAdminUser]

    def delete(self, request, pk):
        palestra = get_object_or_404(Palestra, pk=pk)
        
        palestra.delete()

        return Response(status=status.HTTP_200_OK)


class PalestraEdit(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        palestra = get_object_or_404(Palestra, pk=pk)

        serializer = PalestraSerializer(palestra, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#################################


class FormPost(generics.CreateAPIView):#generics.CreateAPIView

    queryset = Form.objects.all()
    serializer_class = FormSerializer
    '''
    def post(self, request, id):
        palestra = get_object_or_404(Palestra, id=id)  
        return Response({"message": "iha"}, status=status.HTTP_200_OK)
    '''

       # if palestra.favorito.filter(id=request.user.id).exists():
    
    def post(self, request, id):
        if request.user.foi_na_palestra.filter(id=id).exists() and not Form.objects.filter(pa_id=get_object_or_404(Palestra, id=id) ,owner=request.user).exists():
            
            print(request.user.foi_na_palestra.filter(id=id).exists())
            print(Form.objects.filter(pa_id=get_object_or_404(Palestra, id=id) ,owner=request.user).exists())
            
            pergunta1 = request.data['Pergunta1']
            pergunta2 = request.data['Pergunta2']
            pergunta3 = request.data['Pergunta3']
            pergunta4 = request.data['Pergunta4']
            pergunta5 = request.data['Pergunta5']
            palestra = get_object_or_404(Palestra, id=id)  
            usuario = request.user 


            form = Form(Pergunta1=pergunta1,Pergunta2=pergunta2,Pergunta3=pergunta3,Pergunta4=pergunta4,Pergunta5=pergunta5, pa_id=palestra, owner=usuario)
            form.save()
            data = FormSerializer(form).data
            return Response({"message": "Respostas enviadas com sucesso!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Você não pode avaliar essa palestra"}, status=status.HTTP_401_UNAUTHORIZED)

        
    '''
    def perform_create(self, serializer):
        print("OI")
        serializer.save(owner=self.request.user, pa_id = self.request.query_params("id"))
    ''' 

class VerRespostasForms(APIView):
    
    def get(self, request, id):
        form = Form.objects.filter(pa_id=id)
        data = FormSerializer(form, many=True).data
        
        return Response(data)
    


####################################

class FormDetail(APIView):
    def get(self, request, pk):
        form = get_object_or_404(Form, pk=pk)
        data = FormSerializer(form).data

        return Response(data)


class UserList(APIView):
    permission_classes = [IsAdminUser] #DEVE SER ADMIN PARA VER DADOS DOS USUARIOS

    def get(self, request):
        user = User.objects.all()
        data = UserSerializer(user, many=True).data
        
        return Response(data)

class UserDetail(APIView):
    permission_classes = [IsAdminUser] #DEVE SER ADMIN PARA VER DADOS DO USUARIO

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        data = UserSerializer(user).data

        return Response(data)


class UserCreate(generics.CreateAPIView):
    permission_classes = [IsAdminUser] #DEVE SER ADMIN PARA CRIAR O USUÁRIO, POIS QUEREMOS QUE A PESSOA VÁ À BANCADA
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        Token.objects.get_or_create(user=user)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Senha ou email incorreto"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response({"message": "Logout realizado com sucesso!"}, status=status.HTTP_200_OK)


class ValidacaoView(APIView):
    def get(self, request, id):
        palestra = get_object_or_404(Palestra, id=id)

        if palestra.foi_na_palestra.filter(id=request.user.id).exists():
            return Response(data={ "message": "Sua presença já foi contabilizada" }, status=status.HTTP_200_OK)
        else:
            palestra.foi_na_palestra.add(request.user)
            return Response(data={ "message": "Presença contabilizada!" }, status=status.HTTP_200_OK)

class FoiNaPalestraList(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'foinapalestra.html'

    def get(self, request, id):
        users = User.objects.filter(foi_na_palestra=id)
        palestra = get_object_or_404(Palestra, id=id)

        serializer_class = UserSerializer
        permission_classes = [IsAdminUser]
        
        data = UserSerializer(users, many=True).data

        return Response({'palestra': palestra, 'users': users})

class PalPorDia(APIView):

    def get(self, request, date):
        
        #CADA "data" É UMA COISA DIFERENTE, ATENÇÃO

        palestra = Palestra.objects.filter(data=date).order_by('inicio')

        data = PalestraSerializer(palestra, many=True).data

        return Response(data)








'''
pergunta1 = request.data['pergunta1']
pergunta2 = request.data['pergunta2']
pergunta3 = request.data['pergunta3']
pergunta4 = request.data['pergunta4']
pergunta5 = request.data['pergunta5']

form = Form(Pergunta1=pergunta1,Pergunta2=pergunta2,Pergunta3=pergunta3,Pergunta4=pergunta4,Pergunta5=pergunta5)
form.save()
data = FormSerializer(form).data
'''