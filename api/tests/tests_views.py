from rest_framework.test import APITestCase
from rest_framework import status 

from api.models import User, Ativo


class AtivosTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create(username="user", password="abc123")
        cls.usuario.save()

    def setUp(self):
        self.client.force_authenticate(user=self.usuario)

    def test_cadastro_com_nome_e_modalidade_corretos(self):
        """
        Como USUARIO eu gostaria de CADASTRAR UM ATIVO 
        para REAZLIZAR APLICACOES/RESGATES.
        """
        post_data = {'nome': 'BITCOIN', 'modalidade': 'CRIPTO'}
        response = self.client.post('/api/ativos', post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ativo.objects.count(), 1)

    def test_visualizar_todos_ativos_cadastrados(self):
        """
        Como USUARIO eu gostaria de VISUALIZAR TODOS OS ATIVOS
        para SABER AS OPCOES DISPONIVEIS PARA APLICACAO
        """
        ativo_avulso = Ativo.objects.create(nome='BITCOIN', modalidade='CRIPTO')
        ativo_avulso.save()
        response = self.client.get('/api/ativos')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'nome': 'BITCOIN', 'modalidade': 'CRIPTO'})


class OperacoesTestCase(APITestCase):
    # Como um USUARIO eu gostaria de FAZER APLICACOES EM UM ATIVO para INICIAR
    # UM INVESTIMENTO.
    
    # Como um USUARIO eu gostaria de FAZER APLICACOES EM ATIVOS CADASTRADOS POR 
    # OUTROS USUARIOS para visualizar as melhores opcoes de ativos
     
    # Como um USUARIO eu gostaria de FAZER RESGATES EM UM ATIVO para RETIRAR O
    # MEU LUCRO.

    # Usuario nao pode ver aplicacoes de outros usuarios

    # Usuario nao pode ver resgates de outros usuarios
    pass


class CarteiraTestCase(APITestCase):
    # Como um USUARIO eu gostaria de VISUALIZAR O SALDO DA MINHA CARTEIRA DE 
    # INVESTIMENTOS para ACOMPANHAR OS MEUS RESULTADOS.

    # Usuarios nao pode ver saldo na carteira de outros usuarios
    pass