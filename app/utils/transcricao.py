
class Funcoes_de_texto:
    def criarTitulo(self, msg):
        """Essa função cria os titulos ee caminhos para os arquivos de texto finais do programa"""
        title = self.llm.invoke(
            f'Crie um titulo de até três (3) palavras para o texto descrito na mensagem: {msg}'
            f'Esse título deve fazer sentido com todo o conteúdo do texto recebido e deve ser coeso.'
            f'Deve ser relacionado APENAS ao conteúdo do texto'
            f'Utilize apenas termos aceitos para nomear arquivos no computador, nada de Caracteres especiais'
        )
        return title