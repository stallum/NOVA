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

        msg = bot.mostrar_interface()
    
    if msg == "/quit":
        bot.limpar_tela()
        print(f"(N.O.V.A.): ", end='')
        bot.st.typeEffect(msg="Até mais...")
        sleep(2.4)
        bot.limpar_tela()
        sys.exit()
