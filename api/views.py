from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Ativo, Operacao
from .serializers import AtivoSerializer, OperacaoSerializer


class AtivosView(generics.ListCreateAPIView):
	queryset = Ativo.objects.all()
	serializer_class = AtivoSerializer


class OperacoesView(generics.ListCreateAPIView):
	queryset = Operacao.objects.all()
	serializer_class = OperacaoSerializer


class CarteiraView(APIView):
	def get(self, request, format=None):
		return Response()