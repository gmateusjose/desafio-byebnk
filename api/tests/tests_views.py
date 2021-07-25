from rest_framework.test import APITestCase
from rest_framework import status 

from api.models import User, Ativo, Operacao


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
        total_ativos = 1
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ativo.objects.count(), total_ativos)

    def test_visualizar_todos_ativos_cadastrados(self):
        """
        Como USUARIO eu gostaria de VISUALIZAR TODOS OS ATIVOS
        para SABER AS OPCOES DISPONIVEIS PARA APLICACAO
        """
        ativo_avulso = Ativo.objects.create(nome='BITCOIN', modalidade='CRIPTO')
        ativo_avulso.save()
        response = self.client.get('/api/ativos')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'id': 1, 'nome': 'BITCOIN', 'modalidade': 'CRIPTO'}])


class OperacoesTestCase(APITestCase):
    # Como um USUARIO eu gostaria de FAZER APLICACOES EM UM ATIVO para INICIAR
    # UM INVESTIMENTO.
    
    # Como um USUARIO eu gostaria de FAZER APLICACOES EM ATIVOS CADASTRADOS POR 
    # OUTROS USUARIOS para visualizar as melhores opcoes de ativos
     
    # Como um USUARIO eu gostaria de FAZER RESGATES EM UM ATIVO para RETIRAR O
    # MEU LUCRO.

    # Usuario nao pode ver operacoes de outros usuarios
    pass


class CarteiraTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create(username='user', password='abc123')
        cls.usuario.save()

        ativo_avulso = Ativo.objects.create(nome='BITCOIN', modalidade='CRIPTO')
        ativo_avulso.save()

        aplicacao = Operacao.objects.create(
            usuario=cls.usuario,
            operacao='APLICACAO',
            ativo=ativo_avulso,
            quantidade=20,
            preco_unitario_em_centavos=100
        )
        aplicacao.save()

        resgate = Operacao.objects.create(
            usuario=cls.usuario,
            operacao='RESGATE',
            ativo=ativo_avulso,
            quantidade=10,
            preco_unitario_em_centavos=50
        )
        resgate.save()

    def setUp(self):
        self.client.force_authenticate(self.usuario)
        self.response = self.client.get('/api/carteira')

    def test_acessar_carteira(self):
        """
        Como USUARIO gostaria de ACESSAR TODOS OS DADOS REFERENTES A CARTEIRA
        para VER TODAS AS INFORMACOES EM UM UNICO LOCAL
        """
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_visualizar_saldo_carteira(self):
        """
        Como USUARIO gostaria de VISUALIZAR O SALDO DA MINHA CARTEIRA 
        para ACOMPANHAR OS MEUS RESULTADOS.
        """
        saldo_final = 1500
        self.assertEqual(self.response.data['saldo'], saldo_final)
    
    def test_visualizar_total_de_aplicacoes(self):
        """
        Como USUARIO gostaria de VISUALIZAR O TOTAL DE APLICACOES REALIZADAS
        para TER UM ENTENDIMENTO MELHOR DAS OPERACOES
        """
        total_aplicacoes = 1
        self.assertEqual(self.response.data['aplicacoes'], total_aplicacoes)
    
    def test_visualizar_total_de_resgates(self):
        """
        Como USUARIO gostaria de VISUALIZAR O TOTAL DE RESGATES REALIZADOS
        para TER UM ENTENDIMENTO MELHOR DAS OPERACOES
        """
        total_resgates = 1
        self.assertEqual(self.response.data['resgates'], total_resgates)

    def test_usuario_visualizar_apenas_sua_carteira(self):
        """
        Como USUARIO gostaria de VISUALIZAR APENAS A MINHA CARTEIRA
        para ATESTAR A SEGURANCA DA APLICACAO
        """
        nome_usuario = 'user'
        campos_response = ('usuario', 'saldo', 'aplicacoes', 'resgates')
        self.assertEqual(self.response.data['usuario'], nome_usuario)
        self.assertEqual(tuple(self.response.data.keys()), campos_response)