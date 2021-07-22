from django.urls import path
from .views import AtivosView, ResgatesView, AplicacoesView, CarteiraView

urlpatterns = [
    path('ativos', AtivosView.as_view()),
    path('resgates', ResgatesView.as_view()),
    path('aplicacoes', AplicacoesView.as_view()),
    path('carteira', CarteiraView.as_view()),
]