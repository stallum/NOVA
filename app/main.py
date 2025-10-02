from time import sleep

import sys
import os

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from utils.styling import Style


class NOVA: 
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
        self.st = Style()


if __name__ == "__main__":
    bot = NOVA()
    msg = bot.mostrar_interface()  

    while msg != "/quit":

        if msg == "1":
            print("\n \nMe envie o link do vídeo do youtube que quer baixar. ou \"/back\" para voltar ao menu\n")

            link_yt= input("\n(You): ")

            bot.yt.baixarVideo(link_yt)
            sleep(2)
            msg = None
        
        if msg == "2":
            pass

        msg = bot.mostrar_interface()
    
    if msg == "/quit":
        bot.limpar_tela()
        print(f"(N.O.V.A.): ", end='')
        bot.st.typeEffect(msg="Até mais...")
        sleep(2.4)
        bot.limpar_tela()
        sys.exit()


        # st.typeEffect("Qual o diretório onde encontra-se o pdf?\n \n")
            
        # path = input("(YOU): ")

        # print("(NOVA): ", end='')
        # st.typeEffect("Qual o nome do pdf que você quer que eu leia?")

        # arq_name = input("(YOU): ")