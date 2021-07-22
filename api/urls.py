from django.urls import path
from .views import AtivosView

urlpatterns = [
	path('user/ativos', AtivosView.as_view()),
]