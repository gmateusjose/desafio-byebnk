from django.urls import path
from django.urls.conf import re_path
from .views import AtivosView, OperacoesView, CarteiraView

urlpatterns = [
    path('ativos', AtivosView.as_view()),
    re_path('^ativos/(?P<modalidade>.+)/$', AtivosView.as_view()),
    path('operacoes', OperacoesView.as_view()),
    path('carteira', CarteiraView.as_view()),
]
