from langchain_community.document_loaders import PyMuPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

from styling import Style

class PDF():
    def ler_pdf(self, path: str, arq: str):
        self.docs = []
        self.st = Style()

        for n in Path(f"{path}").glob(f"{arq}.pdf"):
            try: 
                loader = PyMuPDFLoader(str(n))
                self.docs.extend(loader.load())
                print(f"arquivo carregado com sucesso: {n.name}")
            except Exception as e:
                print(f"ERROR: {e}")
        
        self.spliter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
        self.chunks = self.spliter.split_documents(self.docs)
        for chunk in self.chunks:
            print(chunk)
            print('-'*30)



if __name__ == "__main__": 
    pdf = PDF()

    # st.typeEffect("Qual o diretório onde encontra-se o pdf?\n \n")
            
    # path = input("(YOU): ")

    # print("(NOVA): ", end='')
    # st.typeEffect("Qual o nome do pdf que você quer que eu leia?")

    # arq_name = input("(YOU): ")

    path = '/home/stallum/Downloads'
    arq_name = 'randomforest2001'

    pdf.ler_pdf(path=path, arq=arq_name)
