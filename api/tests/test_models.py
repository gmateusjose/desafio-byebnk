from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models import Ativo, Operacao, User, Taxa


class ConfiguracaoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ativo_generico = {
            'nome': 'GNC',
            'modalidade': 'CRIPTO',
            'preco_mercado_em_centavos': 100
        }


class TestAtivoModel(ConfiguracaoModelTest):
    def test_criar_ativo_com_modalidades_disponiveis(self):
        """
        Verificar se os Ativos sao criados com sucesso
        """
        modalidades_disponiveis = ['RENDA FIXA', 'RENDA VARIAVEL', 'CRIPTO']
        for modalidade in modalidades_disponiveis:
            self.ativo_generico['modalidade'] = modalidade
            ativo_avulso = Ativo.objects.create(**self.ativo_generico)
            ativo_avulso.save()

        total_ativos = Ativo.objects.count()
        qtd_modalidades = len(modalidades_disponiveis)
        self.assertEqual(total_ativos, qtd_modalidades)

    def test_criar_ativo_com_modalidade_nao_disponivel(self):
        """
        Nao devem ser criados ativos cuja modalidade nao pertencam a lista
        de modalidades disponiveis.
        """
        self.ativo_generico['modalidade'] = 'NOT EXISTENT'
        self.assertRaises(
            ValidationError,
            Ativo.objects.create,
            **self.ativo_generico
        )

    def test_salvar_ativo_com_modalidade_nao_disponivel(self):
        """
        Ativos ja criados nao podem ter modalidade alterada para uma modalidade
        nao disponivel.
        """
        ativo_generico = Ativo.objects.create(**self.ativo_generico)
        ativo_generico.save()
        ativo_generico.modalidade = 'NOT EXISTENT'
        self.assertRaises(ValidationError, ativo_generico.save)


class TestOperacaoModel(ConfiguracaoModelTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        usuario = User.objects.create(username='user', password='abc123')
        usuario.save()

        ativo_generico = Ativo.objects.create(**cls.ativo_generico)
        ativo_generico.save()

        cls.operacao_generica = {
            'usuario': usuario,
            'ativo': ativo_generico,
            'operacao': 'APLICACAO',
            'quantidade': 10,
            'preco_unitario_em_centavos': 100
        }

    def test_criar_operacao_com_operacoes_disponiveis(self):
        """
        Criar operacoes com os tipos 'APLICACAO' e 'RESGATE'.
        """
        operacoes_disponiveis = ['APLICACAO', 'RESGATE']
        for operacao in operacoes_disponiveis:
            self.operacao_generica['operacao'] = operacao
            operacao_generica = Operacao.objects.create(
                **self.operacao_generica
            )
            operacao_generica.save()

        total_operacoes = Operacao.objects.count()
        qtd_operacoes_disponiveis = len(operacoes_disponiveis)
        self.assertEqual(total_operacoes, qtd_operacoes_disponiveis)
        
    def test_criar_operacao_nao_disponivel(self):
        """
        Nao devem ser criadas operacoes cujo tipos nao estejam definidos como
        'APLICACAO' ou 'RESGATE'.
        """
        self.operacao_generica['operacao'] = 'NOT EXISTENT'
        self.assertRaises(
            ValidationError,
            Operacao.objects.create,
            **self.operacao_generica
        )


class TestTaxaModel(ConfiguracaoModelTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.ativo = Ativo.objects.create(**cls.ativo_generico)
        cls.ativo.save()

    def testar_validacao_de_taxa(self):
        """
        A taxa incidida sobre qualquer ativo nao podera ultrapassar 100%
        """
        self.assertRaises(
            ValidationError,
            Taxa.objects.create,
            nome='Taxa Corretagem',
            ativo=self.ativo,
            percentual=150
        )
