import operator, functools
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Sequence, Literal
from langgraph.graph import StateGraph, END, START
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel
from prompts.system_prompts import *
from tools.web_search_tools import *

load_dotenv()

AGENTS = ["Agente_Comunicados_Oficiais", "Agente_Sumarizador"]
OPTIONS = ("FINALIZAR",) + tuple(AGENTS)

NOTICES_TOOLS = [
    read_page
]

model = ChatOpenAI(model="gpt-3.5-turbo")

class RouteResponse(BaseModel):
    next: Literal[OPTIONS]

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str


async def agent_node(state, agent, name):
    try:
        result = await agent.ainvoke(state)
        if isinstance(result, dict) and "messages" in result:
            return {"messages": [AIMessage(content=result["messages"][-1].content, name=name)]}
        return {"messages": [AIMessage(content=str(result), name=name)]}
    except Exception as e:
        return {"messages": [AIMessage(content=f"Ocorreu um erro: {str(e)}", name=name)]}

def supervisor_agent(state):
    prompt = ChatPromptTemplate.from_messages([
        ("system", SUPERVISOR_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Dado a conversa acima, qual agente deve agir em seguida? Selecione uma dessa opções: {options}")
    ]).partial(options=str(OPTIONS), members=", ".join(AGENTS))
    supervisor_chain = prompt | model.with_structured_output(RouteResponse)
    return supervisor_chain.invoke(state)

def output_summarizing_node(state):
    messages = [
        ("system", OUTPUT_SUMMARIZING_SYSTEM_PROMPT),
        (
            "assistant",
            "Por favor sumarize a seguinte informação:\n\n"
            + "\n".join([msg.content for msg in state["messages"]]),
        ),
    ]
    response = model.invoke(messages)
    return {
        "messages": [
            AIMessage(content=response.content, name="Agente_Sumarizador")
        ]
    }

official_notices_agent = create_react_agent(model, tools=NOTICES_TOOLS, state_modifier=OFFICIAL_NOTICES_SYSTEM_PROMPT)
official_notices_node = functools.partial(agent_node, agent=official_notices_agent, name="Agente_Comunicados_Oficiais")



def build_flow() -> StateGraph:
    """
    Constrói o grafo de estados
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("Agente_Supervisor", supervisor_agent)
    workflow.add_node("Agente_Comunicados_Oficiais", official_notices_node)
    workflow.add_node("Agente_Sumarizador", output_summarizing_node)

    workflow.add_edge("Agente_Comunicados_Oficiais", "Agente_Supervisor")
    
    conditional_map = {
        "Agente_Comunicados_Oficiais": "Agente_Comunicados_Oficiais",
        "Agente_Sumarizador": "Agente_Sumarizador",
        "FINALIZAR": "Agente_Sumarizador"
    }
    workflow.add_conditional_edges("Agente_Supervisor", lambda x: x["next"], conditional_map)

    workflow.add_edge("Agente_Sumarizador", END)
    workflow.add_edge(START, "Agente_Supervisor")
    return workflow

def build():
    """
    Costrói o fluxo dos agentes + memory e compila
    """
    memory = MemorySaver()
    workflow = build_flow()
    return workflow.compile(checkpointer=memory)