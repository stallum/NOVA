import os

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import Literal, List, Dict
from langchain_core.messages import SystemMessage, HumanMessage

from video_summarize import YoutubeDownloader
from styling import Style

class MenuOut(BaseModel):
    decisao: Literal["VIDEO_YT", "PDF", "INFO"]
    campos_faltantes: List[str] = Field(default_factory=list)

llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    temperature='0',
    )

PROMPT_MENU = (
    "Você é um triador de service desk do assistente de N.O.V.A. (Núcleo Organizador de Verbetes e Anotações)"
    "Dada a mensagem do usuário, retorne SOMENTE um JSON com:\n"
    "{\n"
    '  "decisao": "VIDEO_YT" | "PDF" | "INFO",\n'
    '  "campos_faltantes": ["..."]\n'
    "}\n"
    "Regras:\n"
    '- **VIDEO_YT**: Pedidos para que você resuma um video, palavras chaves como youtube, video, video aula e derivados\n'
    '- **PDF**: Pedidos que falem para resumir ou ler livros, pdfs, documentos e outros dessa forma.'
    '- **INFO**: Mensagens vagas ou que faltam informações para identificar o tema ou contexto (Ex: "Preciso de ajuda com uma política", "Tenho uma dúvida geral").\n'
    "Analise a mensagem e decida a ação mais apropriada."
    )

menu_chain = llm.with_structured_output(MenuOut)

def triagem(msg: str) -> Dict:
    saida: MenuOut = llm.invoke([
        SystemMessage(content=PROMPT_MENU),
        HumanMessage(content=msg)
        ])
    return saida.model_dump()

teste = [
    "Quero que você resuma um video do youtube",
    "Quero um resumo desse documento para lê-lo mais rápido",
    "Meu professor passou um livro para a gente ler, mas tô sem tempo",
    "Tenho um trabalho para fazer, me ajude."
]

for msg  in teste: 
    print(f'Pergunta: {msg}\n Resposta: {triagem(msg=msg)}')