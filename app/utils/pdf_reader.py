from langchain_community.document_loaders import PyMuPDFLoader

class PDF():
    def carregar_pdf(self, path):
        loader = PyMuPDFLoader(path)
        docs = loader.load()
        return docs[0].page_content

    
if __name__ == "__main__":
    pdf = PDF()

    nome_arquivo = 'Markdown_to_PDF.pdf'
    texto = pdf.carregar_pdf(nome_arquivo)