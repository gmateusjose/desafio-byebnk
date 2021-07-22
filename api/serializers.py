from rest_framework import serializers
from .models import Ativo, Resgate, Aplicacao


class AtivoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ativo
		fields = ('nome', 'modalidade')


class ResgateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Resgate
		fields = ('ativo', 'data_de_solicitacao', 'quantidade', 'preco_unitario_em_centavos')


class AplicacaoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Aplicacao
		fields = ('ativo', 'data_de_solicitacao', 'quantidade', 'preco_unitario_em_centavos')
