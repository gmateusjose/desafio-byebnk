from rest_framework.test import APITestCase
from rest_framework import status

from api.models import User, Ativo, Operacao


class ConfiguracaoDeTestes(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create(username="user", password="abc123")
        cls.usuario.save()
        cls.ativo = Ativo.objects.create(nome="BNB", modalidade='CRIPTO')
        cls.ativo.save()

    def setUp(self):
        self.client.force_authenticate(user=self.usuario)


class AtivosTestCase(ConfiguracaoDeTestes):
    def test_cadastro_com_nome_e_modalidade_corretos(self):
        """
        Como USUARIO eu gostaria de CADASTRAR UM ATIVO para REAZLIZAR 
        APLICACOES/RESGATES.
        """
        novo_total_ativos = 2
        dados_ativo = {'nome': 'BTC', 'modalidade': 'CRIPTO'}
        response = self.client.post('/api/ativos', dados_ativo)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ativo.objects.count(), novo_total_ativos)

    def test_acessar_ativos_usuario(self):
        """
        Como USUARIO gostaria de ACESSAR TODOS OS ATIVOS QUE JA OPEREI para
        COMPREENDER A SITUACAO DOS MEUS INVESTIMENTOS.
        """
        response = self.client.get('/api/ativos')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_visualizar_todos_ativos_cadastrados(self):
        """
        Como USUARIO eu gostaria de VISUALIZAR TODOS OS DADOS DOS ATIVOS para
        SABER AS OPCOES DISPONIVEIS PARA APLICACAO
        """
        response = self.client.get('/api/ativos')
        dados_finais_response = response.data[0]
        self.assertEqual(dados_finais_response['id'], 1)
        self.assertEqual(dados_finais_response['nome'], 'BNB')
        self.assertEqual(dados_finais_response['modalidade'], 'CRIPTO')


class OperacoesTestCase(ConfiguracaoDeTestes):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.dados_base_operacao = {
            'usuario': cls.usuario,
            'ativo': cls.ativo,
            'quantidade': 3,
            'preco_unitario_em_centavos': 100
        }
        operacao_avulsa = Operacao.objects.create(
            operacao="APLICACAO",
            **cls.dados_base_operacao
        )
        operacao_avulsa.save()

    def test_realizar_aplicacao_em_ativo(self):
        """
        Como um USUARIO eu gostaria de FAZER APLICACOES EM UM ATIVO para 
        INICIAR UM INVESTIMENTO
        """
        novo_total_operacoes = 2
        self.dados_base_operacao['ativo'] = self.ativo.id
        self.dados_base_operacao['operacao'] = 'APLICACAO'
        response = self.client.post('/api/operacoes', self.dados_base_operacao)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Operacao.objects.count(), novo_total_operacoes)

    def test_realizar_resgate_em_ativo(self):
        """
        Como um USUARIO eu gostaria de FAZER RESGATES EM UM ATIVO para RETIRAR
        O MEU LUCRO
        """
        novo_total_operacoes = 2
        self.dados_base_operacao['operacao'] = 'RESGATE'
        self.dados_base_operacao['ativo'] = self.ativo.id
        response = self.client.post('/api/operacoes', self.dados_base_operacao)
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

        self.dados_base_operacao['operacao'] = 'APLICACAO'
        self.dados_base_operacao['ativo'] = self.ativo.id
        response = self.client.post('/api/operacoes', self.dados_base_operacao)

        novo_total_operacoes = 2
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


class CarteiraTestCase(ConfiguracaoDeTestes):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        dados_base_operacao = {
            'usuario': cls.usuario,
            'ativo': cls.ativo,
            'quantidade': 20,
            'preco_unitario_em_centavos': 100
        }

        aplicacao = Operacao.objects.create(
            operacao='APLICACAO', 
            **dados_base_operacao
        )
        aplicacao.save()

        dados_base_operacao['quantidade'] = 10
        dados_base_operacao['preco_unitario_em_centavos'] = 50
        resgate = Operacao.objects.create(
            operacao='RESGATE',
            **dados_base_operacao
        )
        resgate.save()

    def setUp(self):
        super().setUp()
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
        saldo_final_manualmente_calculado = 1500
        self.assertEqual(
            self.response.data['saldo'], 
            saldo_final_manualmente_calculado
        )
    
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