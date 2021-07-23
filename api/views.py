from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Ativo, Operacao
from .serializers import AtivoSerializer, OperacaoSerializer


class AtivosView(generics.ListCreateAPIView):
	queryset = Ativo.objects.all()
	serializer_class = AtivoSerializer


class OperacoesView(generics.ListCreateAPIView):
	# Aplicar filter diretamente não funcionaria uma vez que o request não está
	# definido no momento da declaração da classe, e como o request é uma property
	# então request.user.id não funcionaria também, pois request.user não estaria 
	# definido. Uma das soluções possíveis é escrever um queryset base, e depois 
	# o sobreescrever com get_queryset.
	queryset = Operacao.objects.all()
	serializer_class = OperacaoSerializer

	def get_queryset(self):
		return Operacao.objects.filter(usuario=self.request.user)


class CarteiraView(APIView):
	def get(self, request, format=None):
		return Response()