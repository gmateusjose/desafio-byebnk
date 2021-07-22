from django.db import models

class Ativo(models.Model):
	MODALIDADES_DISPONIVEIS = (
		('RENDA FIXA', 'RENDA FIXA'),
		('RENDA VARIAVEL', 'RENDA VARIAVEL'),
		('CRIPTO', 'CRIPTO'),
	)
	nome = models.CharField(max_length=250)
	modalidade = models.CharField(max_length=50, choices=MODALIDADES_DISPONIVEIS)

	def __str__(self):
		return self.nome