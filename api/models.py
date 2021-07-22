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


class Resgate(models.Model):
	ativo = models.ForeignKey('Ativo', on_delete=models.PROTECT)
	data_de_solicitacao = models.DateField(auto_now_add=True)
	quantidade = models.PositiveIntegerField()
	preco_unitario_em_centavos = models.PositiveIntegerField()


class Aplicacao(models.Model):
	ativo = models.ForeignKey('Ativo', on_delete=models.PROTECT)
	data_de_solicitacao = models.DateField(auto_now_add=True)
	quantidade = models.PositiveIntegerField()
	preco_unitario_em_centavos = models.PositiveIntegerField()
