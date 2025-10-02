from time import sleep
import sys
import os

class Style():
    def typeEffect(self, msg: str, delay=0.01):
        for i in msg:
            print(i, end='')
            sys.stdout.flush()
            sleep(delay)
    
    def mostrar_interface(self):
    # Cria o atributo first_run na primeira chamada
        if not hasattr(self, "first_run"):
            self.first_run = True  

        self.limpar_tela()
        ROXO = "\033[1;35m"
        RESET = "\033[0m"
        YELLOW = "\033[1;33m"

        nova = f"""{ROXO}
         _____   _____   _____   _____   
        |   | | |     | |  |  | |  _  |  
        | | | |_|  |  |_|  |  |_|     |_
        |_|___|_|_____|_|\___/|_|__|__|_| 
        {RESET}"""

        desc = f'\n\n{YELLOW}Escolha uma das opções abaixo para proseguir com o programa. ou digite "/quit" para finaliza-lo.{RESET}\n\n'


        # Se for a primeira vez, usa animação
        if self.first_run:
            self.typeEffect(nova, 0.008)
            self.typeEffect(desc, 0.05)
            self.first_run = False  # Marca que já rodou
        else:
            print(nova)
            print(desc)

        msg = input("\n(You): ")
        return msg
    
    def limpar_tela(self):
        os.system("cls" if os.name == "nt" else "clear")
    

if __name__ == "__main__":
    st = Style()
    msg = st.mostrar_interface()
    while msg != "/quit":


        msg = st.mostrar_interface()
    
    if msg == "/quit":
        st.limpar_tela()
        print(f"(N.O.V.A.): ", end='')
        st.typeEffect(msg="Até mais...")
        sleep(2.4)
        st.limpar_tela()
        sys.exit()