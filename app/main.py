from time import sleep

import sys

from utils.styling import Style
from utils.agente import grafo


if __name__ == "__main__":
    bot = Style()
    msg = bot.mostrar_interface()

    while msg != "/quit":        

        decisao = grafo.invoke({"pergunta": msg})
        msg = bot.mostrar_interface()

    
    if msg == "/quit":
        bot.limpar_tela()
        print(f"(N.O.V.A.): ", end='')
        bot.typeEffect(msg="Até mais...")
        sleep(2.4)
        bot.limpar_tela()
        sys.exit()
