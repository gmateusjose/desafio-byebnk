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
    endereco_ip = serializers.SerializerMethodField()

    def get_endereco_ip(self, obj):
        return f"{self.context['request'].META['REMOTE_ADDR']}"
