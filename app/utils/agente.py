from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import Literal, List, Dict, TypedDict, Optional
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

# triagem menu: 

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



# Decisões e Workflow de decisões:

class AgentState(TypedDict, total = False):
    pergunta: str
    triagem: dict
    resposta: Optional[str]
    acao_final: str
 
def node_triagem(state: AgentState) -> AgentState:
    print("Executando nó de triagem...")
    return {"triagem": triagem(state['pergunta'])}


def node_videoYT(state: AgentState) -> AgentState:
    print("Executando nó de videosYt...")

    if state["resposta"] == 'VIDEO_YT':
        update: AgentState = {
            "resposta": "Para resumir o video é necessário que você me mande o link abaixo: \n",
            "acao_final": 'VIDEO_YT'
        }
    
    return update

def node_PDF(state: AgentState) -> AgentState:
    print("Execurando nó de PDF...")

    if state["resposta"] == 'PDF':
        update: AgentState = {
            "resposta": "Para resumir o documento é necessário que você me mande o diretório e nome do arquivo, ou \"*\" para todos os arquivos do diretório: ",
            "acao_final": "PDF"
        }
    
    return update

def node_INFO(state: AgentState) -> AgentState:
    print("Executando o nó de INFO")

    faltantes = state["triagem"].get("campos_faltantes", [])
    detalhe = ','.join(faltantes) if faltantes else "Tema e contexto específico"

    return {
        "resposta": f"Para avançar, preciso que detalhe: {detalhe}",
        "acao_final": "PEDIR_INFO"
    }

def decidir_pos_triagem(state: AgentState) -> str:
    print("Dicidinfo apos a triagem...")
    decisao = state["triagem"]["decisao"]

    if not decisao:
        print("Erro: 'acao_final' não encontrada em triagem:", triagem)
        return "info"

    if decisao == "VIDEO_YT": return "video_yt"
    if decisao == "PDF": return "documento_pdf"
    if decisao == "PEDIR_INFO": return "info"

# langgraph para organizar as tarefas.

workflow = StateGraph(AgentState)

workflow.add_node("triagem", node_triagem)
workflow.add_node("resumir_videoYoutube", node_videoYT)
workflow.add_node("resumir_PDF", node_PDF)
workflow.add_node("pedir_info", node_INFO)

workflow.add_edge(START, "triagem")
workflow.add_conditional_edges("triagem", decidir_pos_triagem, {
    "video_yt": "resumir_videoYoutube",
    "documento_pdf": "resumir_PDF",
    "info": "pedir_info"
})

workflow.add_edge("resumir_videoYoutube", END)
workflow.add_edge("resumir_PDF", END)
workflow.add_edge("pedir_info", END)

grafo = workflow.compile()


if __name__ == "__main__":
    teste = [
        "Quero que você resuma um video do youtube",
        "Quero um resumo desse documento para lê-lo mais rápido",
        "Meu professor passou um livro para a gente ler, mas tô sem tempo",
        "Tenho um trabalho para fazer, me ajude."
    ]

    for msg_test in teste:
        resposta_final = grafo.invoke({"pergunta": msg_test})

        triag = resposta_final.get("triagem", {})
        print(f"PERGUNTA: {msg_test}")
        print(f"DECISÃO: {triag.get('decisao')} | URGÊNCIA: {triag.get('urgencia')} | AÇÃO FINAL: {resposta_final.get('acao_final')}")
        print(f"RESPOSTA: {resposta_final.get('resposta')}")
        if resposta_final.get("citacoes"):
            print("CITAÇÕES:")
            for citacao in resposta_final.get("citacoes"):
                print(f" - Documento: {citacao['documento']}, Página: {citacao['pagina']}")
                print(f"   Trecho: {citacao['trecho']}")

        print("------------------------------------")