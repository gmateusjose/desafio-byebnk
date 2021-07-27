from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Ativo, Operacao, User, Taxa
from .serializers import AtivoSerializer, OperacaoSerializer


class AtivosView(generics.ListCreateAPIView):
    serializer_class = AtivoSerializer

    def get_queryset(self):
        modalidade = self.request.query_params.get('modalidade')
        queryset = Ativo.objects.all()
        if modalidade is not None:
            queryset = queryset.filter(modalidade=modalidade.upper())
        return queryset


class OperacoesView(generics.ListCreateAPIView):
	# Aplicar filter diretamente não funcionaria uma vez que o request não está
	# definido no momento da declaração da classe, e como o request é uma 
    # property então request.user.id não funcionaria também, pois request.user
    # não estaria definido. Uma das soluções possíveis é escrever um queryset
    # base, e depois o sobreescrever com get_queryset.
    queryset = Operacao.objects.all()
    serializer_class = OperacaoSerializer

    def get_queryset(self):
        return Operacao.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        cotas_disponiveis = self.calcula_cotas_disponiveis()
        cotas_requisitadas = int(self.request.data['quantidade'])

        operacao_selecionada = self.request.data['operacao']
        qtd_esta_disponivel = (cotas_disponiveis < cotas_requisitadas)

        if qtd_esta_disponivel and operacao_selecionada == 'RESGATE':
            raise ValidationError('qtd requisitada > qtd disponivel')
        else:
            serializer.save()

    def calcula_cotas_disponiveis(self):
        operacoes_no_ativo = Operacao.objects.filter(
            ativo=self.request.data['ativo'],
            usuario=self.request.user
        )
        sum = 0
        for operacao in operacoes_no_ativo:
            qtd_cotas = operacao.quantidade
            sum += qtd_cotas
        return sum

    def handle_exception(self, exc):
        return Response(
            {'ERROR': 'Cotas solicitadas excedem as cotas disponiveis'},
            status=status.HTTP_400_BAD_REQUEST
        )

		
class CarteiraView(APIView):
    def get(self, request, format=None):
        usuario_atual = User.objects.get(pk=request.user.id)

        aplicacoes_realizadas = self.calcula_aplicacoes_realizadas(request)
        resgates_realizados = self.calcula_resgates_realizados(request)
        preco_mercado_aplicacoes = self.calcular_preco_mercado(
            aplicacoes_realizadas
        )
        preco_mercado_resgates = self.calcular_preco_mercado(resgates_realizados)
		
        saldo = preco_mercado_aplicacoes - preco_mercado_resgates

        preco_unitario_aplicacoes = self.calcular_preco_unitario(aplicacoes_realizadas)
        preco_unitario_resgates = self.calcular_preco_unitario(resgates_realizados)
        precos_unitarios = preco_unitario_aplicacoes - preco_unitario_resgates

        dados_carteira = {
            'usuario': usuario_atual.username, 
            'saldo': saldo,
            'resultado': saldo - precos_unitarios, 
            'aplicacoes': len(aplicacoes_realizadas), 
            'resgates': len(resgates_realizados)
        }
        return Response(dados_carteira)

    def calcula_aplicacoes_realizadas(self, request):
        aplicacoes_realizadas = Operacao.objects.filter(
            operacao='APLICACAO', 
            usuario=request.user.id
        )
        return aplicacoes_realizadas

    def calcula_resgates_realizados(self, request):
        resgates_realizados = Operacao.objects.filter(
            operacao='RESGATE', 
            usuario=request.user.id
		)
        return resgates_realizados
	
    def calcular_preco_mercado(self, operacoes):
        preco_mercado = 0
        for operacao in operacoes:
            ativo = operacao.ativo
            preco = ativo.preco_mercado_em_centavos
            cotas = operacao.quantidade
            taxa = self.calcular_taxa_operacao(operacao.ativo)
            preco_mercado += (cotas * preco) * (1 - taxa)
        return preco_mercado

    def calcular_taxa_operacao(self, ativo):
        taxas_sobre_ativo = Taxa.objects.filter(ativo=ativo)
        total_percentual = sum([taxa.percentual for taxa in taxas_sobre_ativo])
        total_decimal = total_percentual / 100
        return total_decimal

    def calcular_preco_unitario(self, operacoes):
        total = 0
        for operacao in operacoes:
            cotas = operacao.quantidade
            preco = operacao.preco_unitario_em_centavos
            taxa = self.calcular_taxa_operacao(operacao.ativo)
            total += (cotas * preco) * (1 - taxa)
        return total
