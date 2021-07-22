from django.db import models

class Ativo(models.Model):
	nome = models.CharField(max_length=250)
	modalidade = models.CharField(max_length=50)

	def __str__(self):
		return self.nome