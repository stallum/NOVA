import re
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import Literal, List, Dict, TypedDict, Optional
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
import json

# triagem menu: 
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

class MenuOut(BaseModel):
    decisao: Literal["VIDEO_YT", "PDF", "INFO"]
    campos_faltantes: List[str] = Field(default_factory=list)

menu_chain = llm.with_structured_output(MenuOut)

def triagem(msg: str) -> Dict:
    saida: MenuOut = llm.invoke([
        SystemMessage(content=PROMPT_MENU),
        HumanMessage(content=msg)
    ])
    return saida.model_dump()

def decisao_triagem(resposta: str) -> str:
    json_str = re.sub(r'```json|```', '', resposta).strip()
    decisao = json.loads(json_str)['decisao']
    return decisao

class AgentState(TypedDict, total= False):
    pergunta: str
    triagem: dict
    acao_final: str

def node_triagem(state: AgentState) -> AgentState:
    print("Executando nó de triagem...")
    decisao = triagem(state["pergunta"])['content']
    return {"triagem": decisao_triagem(decisao)}

def node_youtube(state: AgentState) -> AgentState:
    print("Executando nó de video do Youtube...")
    return {"acao_final": "video_yt"}

def node_pdf(state: AgentState) -> AgentState:
    print("Executando nó de pdf...")
    return {"acao_final": "PDF"}

def node_mensagem(state: AgentState) -> AgentState:
    print("Executando nó de mensagem...")
    return {"acao_final": "resumir_mensagem"}

def decidir_pos_triagem(state: AgentState) -> str:
    print("Decidindo após a triagem...")
    decisao = state["triagem"]

    return decisao

workflow = StateGraph(AgentState)

workflow.add_node('triagem', node_triagem)
workflow.add_node('youtube', node_youtube)
workflow.add_node('pdf', node_pdf)

workflow.add_edge(START, 'triagem')
workflow.add_conditional_edges(
    'triagem', 
    decidir_pos_triagem,
    {
        "VIDEO_YT": "youtube",
        "PDF": "pdf"
    })
workflow.add_edge('youtube', END)
workflow.add_edge('pdf', END)
grafo = workflow.compile()


if __name__ == "__main__": 
    teste = 'resume esse video para mim'
    decisao = grafo.invoke({"pergunta": teste})

    # resposta = triagem(teste)['content']
    # json_str = re.sub(r'```json|```', '', resposta).strip()
    # decisao = json.loads(json_str)['decisao']

    print(f'{decisao}\n')