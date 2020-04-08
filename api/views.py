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

import qrcode

from django.views.generic import View

from appSFE.utils import render_to_pdf 
from django.template.loader import get_template

User = get_user_model()

#from rest_framework_swagger.views import get_swagger_view
#schema_view = get_swagger_view(title='API')


'''

Comandos para dar dps do git pull no digital ocean

sudo systemctl daemon-reload
sudo systemctl restart gunicorn


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

        serializer = PalestraSerializer(palestra)
        
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
        descricao_palestra = request.data['descricao_palestra']
        palestrante = request.data['palestrante']
        descricao_palestrante = request.data['descricao_palestrante']
        sala = request.data['sala']
        inicio = request.data['inicio']
        termino = request.data['termino']
        data = request.data['dia']
        foto_palestrante = request.data['foto_palestrante']

        postagem = Palestra(tema= tema, termino=termino, descricao_palestra=descricao_palestra, palestrante=palestrante, descricao_palestrante=descricao_palestrante, sala=sala, inicio=inicio, dia=data, foto_palestrante=foto_palestrante)
        postagem.save()
        post = get_object_or_404(Palestra, tema=tema)
        img = qrcode.make('http://67.205.161.203/validar/'+str(post.id)+'/')

        img.save('media/fotos/qrpalestra_'+str(post.id)+'.png')

        '''
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
        '''
        
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

        if User.objects.filter(email=email):
            email_existe = True
        else:
            email_existe = False

        user = authenticate(email=email, password=password)
        if user:
            Token.objects.get_or_create(user=user)
            return Response({"token": user.auth_token.key})
        elif email_existe==False:
            return Response({"error": "Email não cadastrado!"}, status=status.HTTP_400_BAD_REQUEST)
        elif email_existe==True:
            return Response({"error": "Senha incorreta"}, status=status.HTTP_400_BAD_REQUEST)


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

    def get(self, request, id):

        permission_classes = [IsAdminUser]

        users = User.objects.filter(foi_na_palestra=id)
        palestra = get_object_or_404(Palestra, id=id)
        
        userser = UserSerializer(users, many=True).data
        palser = PalestraSerializer(palestra).data

        vectordata = [userser, palser]
        return Response(vectordata)

class PalPorDia(APIView):

    def get(self, request, date):
        
        #CADA "data" É UMA COISA DIFERENTE, ATENÇÃO

        palestra = Palestra.objects.filter(dia=date).order_by('inicio')

        data = PalestraSerializer(palestra, many=True).data

        return Response(data)

class GeneratePdf(APIView):
    def get(self, request, *args, **kwargs):
        
        permission_classes = [IsAdminUser]

        palestras = Palestra.objects.all()
    
        template = get_template('listaqrcode.html')
        data = {
             'palestras': palestras,
        }
        pdf = render_to_pdf('listaqrcode.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

class ParceirosGet(APIView):

    def get(self, request):
        parceiros = Parceiro.objects.all()

        data = ParceiroSerializer(parceiros, many=True).data

        return Response(data)

class ParceiroPost(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        logo = request.data['logo']

        parceiro = Parceiro(logo=logo)
        parceiro.save()
        data = ParceiroSerializer(parceiro).data

        return Response(data)


class ParceiroDelete(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        parceiro = get_object_or_404(Parceiro, pk=pk)
        parceiro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CorPut(APIView):
    permission_classes = [IsAdminUser]
    
    def put(self, request):
        cores = get_object_or_404(Cores, pk=1)

        serializer = CoresSerializer(cores, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CriarObjetoCor(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request):
        primaria = request.data['primaria']
        secundaria = request.data['secundaria']
        terciaria = request.data['terciaria']
        quaternaria = request.data['quaternaria']


        cores = Cores(primaria=primaria, secundaria=secundaria, terciaria=terciaria, quaternaria=quaternaria)
        cores.save()
        data = CoresSerializer(cores).data

        return Response(data)


class GetCor(APIView):
    def get(self, request):
        
        cores = get_object_or_404(Cores, pk=1)

        data = CoresSerializer(cores).data

        return Response(data)

#DA PROXIMA VEZ QUE FIZER UPLOAD VAI DAR ERRO PQ PRECISA DO pip install drf-yasg no servidor