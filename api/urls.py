from django.urls import path
from .views import AtivosView, ResgatesView, AplicacoesView

urlpatterns = [
    path('user/ativos', AtivosView.as_view()),
    path('user/resgates', ResgatesView.as_view()),
    path('user/aplicacoes', AplicacoesView.as_view()),
]