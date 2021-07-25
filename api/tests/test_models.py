from django.test import TestCase

from api.models import Ativo, Operacao, User


class TestAtivoModel(TestCase):
    def test_criar_ativo_com_modalidades_disponiveis(self):
        for modalidade in ['RENDA FIXA', 'RENDA VARIAVEL', 'CRIPTO']:
            ativo_avulso = Ativo.objects.create(nome=f'test {modalidade}', modalidade=f'{modalidade}')
            ativo_avulso.save()
        self.assertEqual(Ativo.objects.count(), 3)

    def test_criar_ativo_com_modalidade_nao_disponivel(self):
        ativo_avulso = Ativo.objects.create(nome=f'test ativo', modalidade='NOT EXISTENT')
        ativo_avulso.save()
        self.assertEqual(Ativo.objects.get().modalidade, 'NOT EXISTENT')


class TestOperacaoModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create(username='user', password='abc123')
        cls.usuario.save()

        cls.ativo_avulso = Ativo.objects.create(nome='BITCOIN', modalidade='CRIPTO')
        cls.ativo_avulso.save()

        cls.quantidade_avulsa = 5
        cls.preco_avulso = 10

    def test_criar_operacao_com_operacoes_disponiveis(self):
        for operacao in ['APLICACAO', 'RESGATE']:
            operacao_avulsa = Operacao.objects.create(
                usuario=self.usuario,
                operacao=operacao,
                ativo=self.ativo_avulso,
                quantidade=self.quantidade_avulsa,
                preco_unitario_em_centavos=self.preco_avulso,
            )
            operacao_avulsa.save()
        self.assertEqual(Operacao.objects.count(), 2)
            

    def test_criar_operacao_nao_disponivel(self):
        operacao_avulsa = Operacao.objects.create(
            usuario=self.usuario,
            operacao='NOT EXISTENT',
            ativo=self.ativo_avulso,
            quantidade=self.quantidade_avulsa,
            preco_unitario_em_centavos=self.preco_avulso,
        )
        operacao_avulsa.save()
        self.assertEqual(Operacao.objects.get().operacao, 'NOT EXISTENT')
