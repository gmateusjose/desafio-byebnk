from rest_framework import generics
from .models import Ativo, Resgate, Aplicacao
from .serializers import AtivoSerializer, ResgateSerializer, AplicacaoSerializer

class AtivosView(generics.ListCreateAPIView):
	queryset = Ativo.objects.all()
	serializer_class = AtivoSerializer


class ResgatesView(generics.ListCreateAPIView):
	queryset = Resgate.objects.all()
	serializer_class = ResgateSerializer


class AplicacoesView(generics.ListCreateAPIView):
	queryset = Aplicacao.objects.all()
	serializer_class = AplicacaoSerializer