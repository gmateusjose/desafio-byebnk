from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Ativo(models.Model):
    MODALIDADES_DISPONIVEIS = (
        ('RENDA FIXA', 'RENDA FIXA'),
        ('RENDA VARIAVEL', 'RENDA VARIAVEL'),
        ('CRIPTO', 'CRIPTO'),
    )
    nome = models.CharField(max_length=250)
    modalidade = models.CharField(
        max_length=15,
        choices=MODALIDADES_DISPONIVEIS
    )
    preco_mercado_em_centavos = models.PositiveIntegerField()

    def __str__(self):
        return self.nome

    def clean(self):
        tupla_modalidades = (self.modalidade, self.modalidade)
        if tupla_modalidades not in self.MODALIDADES_DISPONIVEIS:
            raise ValidationError({'modalidade': 'Modalidade does not exist'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Operacao(models.Model):
    OPERACOES_DISPONIVEIS = (
        ('APLICACAO', 'APLICACAO'),
        ('RESGATE', 'RESGATE'),
    )
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    operacao = models.CharField(max_length=10, choices=OPERACOES_DISPONIVEIS)
    ativo = models.ForeignKey('Ativo', on_delete=models.PROTECT)
    data_de_solicitacao = models.DateField(auto_now_add=True)
    quantidade = models.PositiveIntegerField()
    preco_unitario_em_centavos = models.PositiveIntegerField()
    endereco_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f'Operacao {self.id}'

    def clean(self):
        tupla_operacoes = (self.operacao, self.operacao)
        if tupla_operacoes not in self.OPERACOES_DISPONIVEIS:
            raise ValidationError({'operacao': 'operacao does not exist'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Taxa(models.Model):
    nome = models.CharField(max_length=64)
    ativo = models.ForeignKey('Ativo', on_delete=models.PROTECT)
    percentual = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)]
    )

    def __str__(self):
        return f"{self.nome.title()}"

    def clean(self):
        if self.percentual > 100:
            raise ValidationError("Percentual must be less than or \
                equals to 100")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
