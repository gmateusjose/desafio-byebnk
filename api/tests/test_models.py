from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models import Ativo, Operacao, User


class TestAtivoModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.nome_ativo = 'ATIVO TESTE'
        cls.modalidades_disponiveis = [
            'RENDA FIXA', 
            'RENDA VARIAVEL', 
            'CRIPTO'
        ]

    def test_criar_ativo_com_modalidades_disponiveis(self):
        """
        Verificar se os Ativos sao criados com sucesso
        """
        for modalidade in self.modalidades_disponiveis:
            ativo_avulso = Ativo.objects.create(
                nome=self.nome_ativo, 
                modalidade=modalidade
            )
            ativo_avulso.save()
        total_ativos = Ativo.objects.count()
        self.assertEqual(total_ativos, len(self.modalidades_disponiveis))

    def test_criar_ativo_com_modalidade_nao_disponivel(self):
        """
        Nao devem ser criados ativos cuja modalidade nao pertencam a lista
        de modalidades disponiveis.
        """
        self.assertRaises(
            ValidationError, 
            Ativo.objects.create, 
            nome=self.nome_ativo, 
            modalidade='NOT EXISTENT'
        )
    
    def test_salvar_ativo_com_modalidade_nao_disponivel(self):
        """
        Ativos ja criados nao podem ter modalidade alterada para uma modalidade
        nao disponivel.
        """
        ativo_avulso = Ativo.objects.create(
            nome=self.nome_ativo, 
            modalidade='CRIPTO'
        )
        ativo_avulso.save()
        ativo_avulso.modalidade = 'NOT EXISTENT'
        self.assertRaises(ValidationError, ativo_avulso.save)


class TestOperacaoModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        usuario = User.objects.create(username='user', password='abc123')
        ativo_avulso = Ativo.objects.create(nome='BNB', modalidade='CRIPTO')
        usuario.save() 
        ativo_avulso.save()
        cls.operacoes_disponiveis = ['APLICACAO', 'RESGATE']
        cls.dados_base = {
            'usuario': usuario,
            'ativo': ativo_avulso,
            'quantidade': 10,
            'preco_unitario_em_centavos': 5
        }

    def test_criar_operacao_com_operacoes_disponiveis(self):
        """
        Criar operacoes com os tipos 'APLICACAO' e 'RESGATE'.
        """
        for operacao in self.operacoes_disponiveis:
            operacao_avulsa = Operacao.objects.create(
                operacao=operacao, 
                **self.dados_base
            )
            operacao_avulsa.save()
        total_operacoes=Operacao.objects.count()
        self.assertEqual(total_operacoes, len(self.operacoes_disponiveis))
            
    def test_criar_operacao_nao_disponivel(self):
        """
        Nao devem ser criadas operacoes cujo tipos nao estejam definidos como
        'APLICACAO' ou 'RESGATE'.
        """
        self.assertRaises(
            ValidationError, 
            Operacao.objects.create, 
            operacao='NOT EXISTENT', 
            **self.dados_base
        )