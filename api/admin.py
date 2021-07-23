from django.contrib import admin
from .models import Ativo, Operacao


class AtivoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'modalidade')


class OperacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'operacao', 'ativo')


admin.site.register(Ativo, AtivoAdmin)
admin.site.register(Operacao, OperacaoAdmin)