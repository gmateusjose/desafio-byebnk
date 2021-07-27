from django.contrib import admin
from .models import Ativo, Operacao, Taxa


class AtivoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'modalidade')


class OperacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'operacao', 'ativo')


class TaxaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo', 'percentual')


admin.site.register(Ativo, AtivoAdmin)
admin.site.register(Operacao, OperacaoAdmin)
admin.site.register(Taxa, TaxaAdmin)
