from rest_framework import serializers
from .models import Ativo, Operacao


class AtivoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ativo
		fields = ('nome', 'modalidade')


class OperacaoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Operacao
		fields = (
			'operacao', 
			'ativo', 
			'data_de_solicitacao', 
			'quantidade', 
			'preco_unitario_em_centavos',
		)