from django.contrib import admin
from .models import Ativo, Resgate, Aplicacao

admin.site.register(Ativo)
admin.site.register(Resgate)
admin.site.register(Aplicacao)