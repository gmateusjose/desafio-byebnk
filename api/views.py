from rest_framework import generics
from .models import Ativo
from .serializers import AtivoSerializer

class AtivosView(generics.ListCreateAPIView):
	queryset = Ativo.objects.all()
	serializer_class = AtivoSerializer