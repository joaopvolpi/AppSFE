from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.permissions import * 
from rest_framework import status
from django.contrib.auth import get_user_model
from django.views.generic import View

User = get_user_model()

class FavoriteView(APIView):
    def get(self, request, id):
        palestra = get_object_or_404(Palestra, id=id)
        if palestra.favorito.filter(id=request.user.id).exists():
            palestra.favorito.remove(request.user.id)
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
        data = PalestraSerializer(postagem).data
        return Response(data)

class PalestraDelete(APIView):
    permission_classes  = [IsAdminUser]
    def delete(self, request, pk):
        palestra = get_object_or_404(Palestra, pk=pk)
        palestra.delete()
        return Response(status=status.HTTP_200_OK)

class UserList(APIView):
    permission_classes = [IsAdminUser] #DEVE SER ADMIN PARA VER DADOS DOS USUARIOS
    def get(self, request):
        user = User.objects.all()
        data = UserSerializer(user, many=True).data
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

class LoginAdminView(APIView):
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
            if user.is_staff:
                Token.objects.get_or_create(user=user)
                return Response({"token": user.auth_token.key})
            else:
                return Response({"error": "Você não tem autorização"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Dados incorretos"}, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response({"message": "Logout realizado com sucesso!"}, status=status.HTTP_200_OK)

class ValidacaoView(APIView):
    def get(self, request, tema):
        palestra = get_object_or_404(Palestra, tema=tema)

        if palestra.foi_na_palestra.filter(id=request.user.id).exists():
            return Response(data={ "message": "Sua presença já foi contabilizada" }, status=status.HTTP_200_OK)
        else:
            palestra.foi_na_palestra.add(request.user)
            return Response(data={ "message": "Presença contabilizada!" }, status=status.HTTP_200_OK)

class FoiNaPalestraList(APIView):
    def get(self, request, id):
        permission_classes = [IsAdminUser]
        palestra = get_object_or_404(Palestra, id=id)
        users = User.objects.filter(foi_na_palestra=id)
        data = UserSerializer(users, many=True).data
        return Response(data)

class PalPorDia(APIView):
    def get(self, request, date):
        #CADA "data" É UMA COISA DIFERENTE, ATENÇÃO
        palestra = Palestra.objects.filter(dia=date).order_by('inicio')
        data = PalestraSerializer(palestra, many=True).data
        return Response(data)

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
        #A COR É SOMENTE EDITADA, NÃO ADICIONADA, POR ISSO O pk=1
        cores = get_object_or_404(Cores, pk=1)  
        serializer = CoresSerializer(cores, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CriarObjetoCor(APIView):
    #Essa view só deve ser usada uma vez, pq ela cria o objeto cor pra guardar no bd, que dps só vai ser editado pra mudar as cores
    permission_classes = [IsAdminUser]
    def post(self, request):
        primaria = request.data['primaria']
        secundaria = request.data['secundaria']
        terciaria = request.data['terciaria']
        dark_terciaria = request.data['dark_terciaria']
        quaternaria = request.data['quaternaria']
        texto = request.data['texto']
        cores = Cores(primaria=primaria, secundaria=secundaria, terciaria=terciaria, dark_terciaria= dark_terciaria, quaternaria=quaternaria, texto=texto)
        cores.save()
        data = CoresSerializer(cores).data
        return Response(data)

class GetCor(APIView):
    def get(self, request):
        cores = get_object_or_404(Cores, pk=1)
        data = CoresSerializer(cores).data
        return Response(data)        

class CriarObjetoDia(APIView):
    #Essa view só deve ser usada uma vez, pq ela cria o objeto dia pra guardar no bd, que dps só vai ser editado pra mudar os dias
    permission_classes = [IsAdminUser]
    def post(self, request):
        pri = request.data['pri']
        seg = request.data['seg']
        ter = request.data['ter']
        qua = request.data['qua']
        qui = request.data['qui']
        dias = Dias(pri=pri, seg=seg, ter=ter, qua=qua, qui=qui)
        dias.save()
        data = DiasSerializer(dias).data
        return Response(data)

class GetDias(APIView):
    def get(self, request):
        dias = get_object_or_404(Dias, pk=1)
        data = DiasSerializer(dias).data
        return Response(data)

class DiasPut(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request):
        #O DIA É SOMENTE EDITADO, NÃO ADICIONADO, POR ISSO O pk=1
        dias = get_object_or_404(Dias, pk=1)  
        serializer = DiasSerializer(dias, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteGeral(APIView):
    permission_classes  = [IsAdminUser]
    def delete(self, request):
        users = User.objects.filter(is_superuser=False)
        users.delete()
        palestras = Palestra.objects.all()
        palestras.delete()
        parceiros = Parceiro.objects.all()
        parceiros.delete()
        return Response(data={ "message": "Tudo foi deletado!" },status=status.HTTP_200_OK)