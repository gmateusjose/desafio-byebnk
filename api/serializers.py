from rest_framework import serializers

from .models import Ativo, Operacao


class AtivoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ativo
		fields = '__all__'


class OperacaoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Operacao
		fields = '__all__'

	usuario = serializers.HiddenField(
		default=serializers.CurrentUserDefault()
	)