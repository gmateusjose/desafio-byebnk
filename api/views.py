from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Ativo, Operacao, User
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
		usuario_atual = User.objects.get(pk=request.user.id)
		aplicacoes_realizadas = Operacao.objects.filter(operacao='APLICACAO', usuario=request.user.id)
		resgates_realizados = Operacao.objects.filter(operacao='RESGATE', usuario=request.user.id)

		sum_aplicacoes = 0
		for aplicacao in aplicacoes_realizadas:
			sum_aplicacoes += (aplicacao.quantidade * aplicacao.preco_unitario_em_centavos)

		sum_resgates = 0
		for resgate in resgates_realizados:
			sum_resgates += (resgate.quantidade * resgate.preco_unitario_em_centavos)

		dados_carteira = {
			'usuario': usuario_atual.username, 
			'saldo': sum_aplicacoes - sum_resgates, 
			'aplicacoes': len(aplicacoes_realizadas), 
			'resgates': len(resgates_realizados)
		}
		return Response(dados_carteira)