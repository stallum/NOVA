from langchain_community.document_loaders import PyMuPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List

class PDF():
    def __init__(self, pdfs_path: Path):
        """
        Inicializa o leitor de PDF.
        :param pdfs_path: O caminho para o diretório contendo os arquivos PDF.
        """
        if not pdfs_path.is_dir():
            raise FileNotFoundError(f"O diretório de PDFs não foi encontrado: {pdfs_path}")
        self.pdfs_path = pdfs_path
        self.docs = []
        self.chunks = []

    def carregar_documentos(self, glob_pattern: str = "*.pdf") -> List:
        """
        Carrega documentos PDF de um diretório.
        :param glob_pattern: Padrão para encontrar os arquivos (ex: '*.pdf' para todos).
        :return: Uma lista de documentos carregados.
        """
        self.docs = []
        for pdf_file in self.pdfs_path.glob(glob_pattern):
            try: 
                loader = PyMuPDFLoader(str(pdf_file))
                self.docs.extend(loader.load())
                print(f"Arquivo carregado com sucesso: {pdf_file.name}")
            except Exception as e:
                print(f"Erro ao carregar {pdf_file.name}: {e}")
        return self.docs

    def dividir_em_chunks(self, chunk_size: int = 300, chunk_overlap: int = 30) -> List:
        """Divide os documentos carregados em chunks."""
        if not self.docs:
            print("Nenhum documento carregado para dividir.")
            return []
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.chunks = splitter.split_documents(self.docs)
        return self.chunks

if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    PDFS_DIR = PROJECT_ROOT / "_pdfs"
    
    pdf_reader = PDF(pdfs_path=PDFS_DIR)
    pdf_reader.carregar_documentos()
    chunks = pdf_reader.dividir_em_chunks()
    print(f"\nTotal de {len(chunks)} chunks criados.")
    for i, chunk in enumerate(chunks[:]): # Imprime os 3 primeiros chunks como exemplo
        print(f"\n--- Chunk {i+1} ---")
        print(chunk.page_content)
