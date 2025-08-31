from time import sleep

import sys
import os

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import GoogleGenerativeAI


class NOVA: 
    def __init__(self):
        self.llm = GoogleGenerativeAI(model="gemini-2.5-flash-lite")


    def criarTitulo(self, msg):
        """Essa função cria os titulos ee caminhos para os arquivos de texto finais do programa"""
        title = self.llm.invoke(
            f'Crie um titulo de até três (3) palavras para o texto descrito na mensagem: {msg}'
            f'Esse título deve fazer sentido com todo o conteúdo do texto recebido e deve ser coeso.'
            f'Deve ser relacionado APENAS ao conteúdo do texto'
            f'Utilize apenas termos aceitos para nomear arquivos no computador, nada de Caracteres especiais'
        )
        return title
    
    def typeEffect(self, msg, delay="0.01"):
        for i in msg:
            print(i, end='')
            sys.stdout.flush()
            sleep(delay)
    
    def limpar_tela(self):
        os.system("cls" if os.name == "nt" else "clear")

    def mostrar_interface(self):
        self.limpar_tela()
        ROXO = "\033[1;35m"
        RESET = "\033[0m"
        YELLOW = "\033[1;33m"


        vega = f"""{ROXO}
         __    _        _______        __   __        _______       
        |  |  | |      |       |      |  | |  |      |   _   |      
        |   |_| |      |   _   |      |  |_|  |      |  |_|  |      
        |       |      |  | |  |      |       |      |       |      
        |  _    | ___  |  |_|  | ___  |       | ___  |       | ___  
        | | |   ||   | |       ||   |  |     | |   | |   _   ||   | 
        |_|  |__||___| |_______||___|   |___|  |___| |__| |__||___| 

        {RESET}"""

        desc = f'{YELLOW}Escolha uma das opções abaixo para proseguir com o programa. ou digite "/quit" para finaliza-lo.{RESET}'

        menu = f"""{YELLOW}
        MENU DE OPÇÕES: 
        [1] RESUMIR VIDEO YOUTUBE
        [2] RESUMIR PDF
        [3] INSERIR TEXTO
        
        {RESET}
        """

        
        self.typeEffect(vega, 0.008)
        self.typeEffect(desc, 0.05)

        print(menu)
        msg = input("(You): ")
        return msg
    


if __name__ == "__main__":
    bot = NOVA()
    msg = bot.mostrar_interface()

    if msg == "/quit": 
        print(f"(N.O.V.A.): ", end='')
        for i in "Até mais...":
            print(i, end='')
            sys.stdout.flush()
            sleep(0.01)

    elif msg == "1":
        pass
    