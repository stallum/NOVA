from langchain_google_genai import ChatGoogleGenerativeAI

import os
from dotenv import load_dotenv
load_dotenv()

class Notas:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)

    def criar_titulo(self, msg):
        """Essa função cria os titulos ee caminhos para os arquivos de texto finais do programa"""
        print('Criando título...')
        title = self.llm.invoke(
            f'Crie um titulo de até três (3) palavras para o texto descrito na mensagem: {msg}'
            f'Esse título deve fazer sentido com todo o conteúdo do texto recebido e deve ser coeso.'
            f'Deve ser relacionado APENAS ao conteúdo do texto'
            f'Utilize apenas termos aceitos para nomear arquivos no computador, nada de Caracteres especiais'
        )
        return title
    
    def criar_tags(self, texto):
        """ Essa função tem o objetivo de criar as tags da nota """
        print('Criando tags...')

        tags = self.llm.invoke(
            f'Crie até 10 tags referentes a este texto: \n{texto}\n'
            f'Voce deve responder apenas as tags, sem nenhum comentario, nem numeração'
            f'as tags devem estar alinhadas em uma unica linha, separadas por um espaço'
            f'Elas devem ser relacionadas apenas ao conteudo do texto'
            f'por exemplo, um texto que fale sobre filosofia pode ter a tag #filosofia'
            f'outro exemplo, um texto que fale sobre treino de academia pode ter as tags #fitness #health'
            f'todas a tags devem ter # na frente, por exemplo: #exemplo'
        )
        return tags.content
        
    def criar_resumos(self, texto):
        """ Essa função cria resumos detalhados sobre o conteúdo entregue para a nota"""
        print('Criando Resumo do texto')

        resumo = self.llm.invoke(
            f'Resuma detalhadamente o texto:  \n{texto}\n'
            f'mantendo todas as informações importantes de forma estruturada'
            f'o Resumo deve conter todas as informações para que uma pessoa que não leu o texto orignal possa entender por completo'
            f'Faça para que seja possível ler, entender e estudar de maneira mais aprofundada quando quiser'
            f'O resultado final deve estar em português brasileiro e formatado em Markdown.'
        )
        return resumo.content
    
    def formatar_nota(self, tags, resumo):
        """Essa função formata os textos em uma unica nota com título, #tags, os resumos."""
        print('Formatando texto...')
        texto_final = (
            f'{tags}\n\n'
            f'## Resumo Detalhado\n{resumo}\n\n'
        )
        return texto_final
    
    def criar_nota(self, msg):
        """Essa função salva o texto em um arquivo de texto no diretório _notas."""
        print('Criando nota em arquivo')

        output_path = os.getenv('OBSIDIAN_PATH')

        tags = self.criar_tags(msg)
        resumo = self.criar_resumos(msg)
        nota = self.formatar_nota(tags, resumo)
        titulo = self.criar_titulo(resumo)
        print('Nota criada.\n\n')
        

        texto_path = os.path.join(output_path, f'{titulo.content}.md')

        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"Criada pasta '_notas' em: {output_path}")
        
        with open(texto_path, 'w', encoding='utf-8') as f:
            f.write(nota)
        print(f"Nota salva em: {texto_path}")


if __name__ == '__main__':
    texto = """
    A computação quântica é um dos campos mais promissores da ciência e tecnologia moderna. Diferente da computação clássica, que utiliza bits representados por 0 ou 1, a computação quântica faz uso de qubits, que podem assumir simultaneamente os estados 0 e 1 devido ao princípio da superposição quântica. Essa propriedade, combinada com o entrelaçamento quântico, permite processar uma quantidade massiva de informações em paralelo, aumentando exponencialmente a capacidade de resolver certos tipos de problemas.

    Os computadores quânticos ainda estão em estágios iniciais de desenvolvimento, mas já apresentam potenciais aplicações em áreas como simulação de moléculas, otimização de processos industriais, criptografia avançada e inteligência artificial. Uma das áreas em que se espera grande impacto é justamente o Machine Learning (ML).

    O Machine Learning é um ramo da inteligência artificial voltado para a criação de algoritmos capazes de aprender padrões a partir de dados. Ele já está presente em nosso cotidiano em recomendações de filmes, reconhecimento de voz, diagnósticos médicos auxiliados por IA e sistemas de previsão. Porém, o aprendizado de máquina enfrenta desafios quando o volume e a complexidade dos dados aumentam, exigindo grande poder de processamento.

    É nesse ponto que a computação quântica pode transformar o cenário. Os algoritmos quânticos podem acelerar o treinamento de modelos de ML, reduzir o tempo de processamento e permitir a análise de bases de dados muito maiores do que as possíveis com máquinas clássicas. Técnicas como o Quantum Machine Learning (QML) estão sendo desenvolvidas para explorar o potencial dos qubits na melhoria de modelos de classificação, regressão e reconhecimento de padrões.

    Um exemplo é o uso de algoritmos quânticos para otimização, uma tarefa central no treinamento de redes neurais. Enquanto computadores clássicos precisam testar muitas combinações para encontrar soluções ideais, os computadores quânticos podem explorar múltiplos caminhos simultaneamente, acelerando o processo. Além disso, aplicações em clustering, redução de dimensionalidade e simulação de sistemas complexos já começam a surgir em pesquisas experimentais.

    Apesar do potencial, existem desafios significativos. Os computadores quânticos atuais são frágeis, sujeitos a ruídos e erros, o que limita sua aplicação prática em larga escala. A área ainda depende de avanços em hardware, correção de erros quânticos e no desenvolvimento de algoritmos híbridos que combinem o poder da computação clássica e quântica.

    Em resumo, a computação quântica e o machine learning representam a convergência de duas áreas revolucionárias. Juntas, elas prometem abrir caminho para soluções mais rápidas, precisas e eficientes, impactando desde a ciência básica até setores econômicos inteiros. Embora ainda estejamos nos primeiros passos, o futuro aponta para um mundo em que inteligência artificial e qubits trabalharão lado a lado, expandindo os limites do que hoje consideramos possível.
    """
    notas = Notas()
    notas.criar_nota(msg=texto)