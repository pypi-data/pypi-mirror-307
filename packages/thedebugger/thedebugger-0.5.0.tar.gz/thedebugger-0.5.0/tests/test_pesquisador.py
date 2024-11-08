import unittest
from learnfetch.pesquisador import Pesquisador

class TestPesquisador(unittest.TestCase):
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.pesquisador = Pesquisador()

    def test_get_response(self):
        """Teste básico do método get_response"""
        resultado = self.pesquisador.get_response("Fotossíntese")
        self.assertIsInstance(resultado, list)
        self.assertGreater(len(resultado), 0)
        
    def test_get_response_conteudo(self):
        """Teste para verificar o conteúdo do resultado"""
        resultado = self.pesquisador.get_response("Fotossíntese")
        self.assertIsInstance(resultado[0], dict)
        self.assertIn("title", resultado[0])
        
    # Adicione mais testes conforme necessário

if __name__ == '__main__':
    unittest.main()
