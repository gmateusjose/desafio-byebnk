from django.urls import path
from .views import AtivosAPIView

urlpatterns = [
	path('user/ativos', AtivosAPIView.as_view()),
]