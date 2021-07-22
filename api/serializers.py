from rest_framework import serializers
from .models import Ativo

class AtivoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ativo
		fields = ('nome', 'modalidade')