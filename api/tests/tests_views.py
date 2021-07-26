from rest_framework.test import APITestCase
from rest_framework import status

from api.models import User, Ativo, Operacao


class AtivosTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create(username="user", password="abc123")
        cls.usuario.save()
        cls.dados_ativo = {'nome': 'BITCOIN', 'modalidade': 'CRIPTO'}

    def setUp(self):
        self.client.force_authenticate(user=self.usuario)

    def test_cadastro_com_nome_e_modalidade_corretos(self):
        """
        Como USUARIO eu gostaria de CADASTRAR UM ATIVO para REAZLIZAR 
        APLICACOES/RESGATES.
        """
        novo_total_ativos = 1
        response = self.client.post('/api/ativos', self.dados_ativo)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ativo.objects.count(), novo_total_ativos)

    def test_visualizar_todos_ativos_cadastrados(self):
        """
        Como USUARIO eu gostaria de VISUALIZAR TODOS OS ATIVOS para SABER AS 
        OPCOES DISPONIVEIS PARA APLICACAO
        """
        ativo_avulso = Ativo.objects.create(**self.dados_ativo)
        ativo_avulso.save()
        response = self.client.get('/api/ativos')
        dados_finais = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dados_finais['id'], 1)
        self.assertEqual(dados_finais['nome'], 'BITCOIN')
        self.assertEqual(dados_finais['modalidade'], 'CRIPTO')


class OperacoesTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create(username='user', password='abc123')
        cls.ativo_avulso = Ativo.objects.create(
            nome="BITCOIN", 
            modalidade="CRIPTO"
        )
        cls.usuario.save()        
        cls.ativo_avulso.save()

        operacao_avulsa = Operacao.objects.create(
            usuario=cls.usuario,
            operacao="APLICACAO",
            ativo=cls.ativo_avulso,
            quantidade=3,
            preco_unitario_em_centavos=100

        )
        operacao_avulsa.save()

    def setUp(self):
        self.client.force_authenticate(user=self.usuario)

    def test_realizar_aplicacao_em_ativo(self):
        """
        Como um USUARIO eu gostaria de FAZER APLICACOES EM UM ATIVO para 
        INICIAR UM INVESTIMENTO
        """
        post_data = {
            'operacao': 'APLICACAO',
            'ativo': self.ativo_avulso.id,
            'quantidade': 10,
            'preco_unitario_em_centavos': 500,
        }
        novo_total_operacoes = 2
        response = self.client.post('/api/operacoes', post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Operacao.objects.count(), novo_total_operacoes)

    def test_realizar_resgate_em_ativo(self):
        """
        Como um USUARIO eu gostaria de FAZER RESGATES EM UM ATIVO para RETIRAR
        O MEU LUCRO
        """
        post_data = {
            'operacao': 'RESGATE',
            'ativo': self.ativo_avulso.id,
            'quantidade': 10,
            'preco_unitario_em_centavos': 200,
        }
        novo_total_operacoes = 2
        response = self.client.post('/api/operacoes', post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Operacao.objects.count(), novo_total_operacoes)

    def test_realizar_aplicacao_em_ativo_de_outro_usuario(self):
        """
        Como USUARIO eu gostaria de FAZER APLICACOES EM UM ATIVO DE OUTRO 
        USUARIO para RETIRAR O MEU LUCRO.
        """
        second_user = User.objects.create(username='user2', password='abc123')
        second_user.save()
        self.client.force_authenticate(user=second_user)        
        post_data = {'nome': 'CDB', 'modalidade': 'RENDA FIXA'}
        self.client.post('/api/ativos', post_data)
        self.client.force_authenticate(user=self.usuario)
        post_data = {
            'operacao': 'APLICACAO',
            'ativo': Ativo.objects.get(nome='CDB').id,
            'quantidade': 5,
            'preco_unitario_em_centavos': 30,
        }
        novo_total_operacoes = 2
        response = self.client.post('/api/operacoes', post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Operacao.objects.count(), novo_total_operacoes)

    def test_usuario_visualiza_apenas_suas_operacoes(self):
        """
        Como USUARIO eu gostaria de VISUALIZAR APENAS MINHAS OPERACOES
        para ATESTAR A SEGURANCA DA APLICACAO
        """
        response = self.client.get('/api/operacoes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        for response_item in response.data:
            operacao_id = response_item['id']
            operacao = Operacao.objects.get(pk=operacao_id)
            self.assertEqual(operacao.usuario.id, self.usuario.id)


class CarteiraTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create(username='user', password='abc123')
        ativo_avulso = Ativo.objects.create(nome='BITCOIN', modalidade='CRIPTO')
        cls.usuario.save()
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
        Como USUARIO gostaria de VISUALIZAR O SALDO DA MINHA CARTEIRA para 
        ACOMPANHAR OS MEUS RESULTADOS.
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
        Como USUARIO gostaria de VISUALIZAR O TOTAL DE RESGATES REALIZADOS para
        TER UM ENTENDIMENTO MELHOR DAS OPERACOES
        """
        total_resgates = 1
        self.assertEqual(self.response.data['resgates'], total_resgates)

    def test_usuario_visualizar_apenas_sua_carteira(self):
        """
        Como USUARIO gostaria de VISUALIZAR APENAS A MINHA CARTEIRA para 
        ATESTAR A SEGURANCA DA APLICACAO
        """
        nome_usuario = 'user'
        self.assertEqual(self.response.data['usuario'], nome_usuario)