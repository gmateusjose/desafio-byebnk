from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Ativo, Resgate, Aplicacao
from .serializers import AtivoSerializer, ResgateSerializer
from .serializers import AplicacaoSerializer


class CarteiraView(APIView):
	def get(self, request, format=None):
		return Response()


class AtivosView(generics.ListCreateAPIView):
	queryset = Ativo.objects.all()
	serializer_class = AtivoSerializer


class ResgatesView(generics.ListCreateAPIView):
	queryset = Resgate.objects.all()
	serializer_class = ResgateSerializer


class AplicacoesView(generics.ListCreateAPIView):
	queryset = Aplicacao.objects.all()
	serializer_class = AplicacaoSerializer