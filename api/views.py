from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Ativo, Operacao, User
from .serializers import AtivoSerializer, OperacaoSerializer


# TODO: NAO PERMITIR QUE SEJA FEITA MAIS RESGATES DO QUE APLICACOES, IMPEDINDO O
# SALDO NEGATIVO!!!

# TODO: IMPLEMENTAR NOVO MODELO DE CARTEIRA, QUE MOSTRA O SALDO ATUAL SEGUNDO O 
# MERCADO E O LUCRO OU PREJUIZO DA CARTEIRA DO USUARIO.

class AtivosView(generics.ListCreateAPIView):
	serializer_class = AtivoSerializer

	def get_queryset(self):
		queryset = Ativo.objects.all()
		modalidade = self.request.query_params.get('modalidade')
		if modalidade is not None:
			queryset = queryset.filter(modalidade=modalidade.upper())
		return queryset


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
		aplicacoes_realizadas = Operacao.objects.filter(
			operacao='APLICACAO', 
			usuario=request.user.id
		)
		resgates_realizados = Operacao.objects.filter(
			operacao='RESGATE', 
			usuario=request.user.id
		)
		produto = lambda operacoes: \
			[op.quantidade * op.preco_unitario_em_centavos for op in operacoes]
		sum_resgates = sum(produto(resgates_realizados))
		sum_aplicacoes = sum(produto(aplicacoes_realizadas))

		dados_carteira = {
			'usuario': usuario_atual.username, 
			'saldo': sum_aplicacoes - sum_resgates, 
			'aplicacoes': len(aplicacoes_realizadas), 
			'resgates': len(resgates_realizados)
		}
		return Response(dados_carteira)