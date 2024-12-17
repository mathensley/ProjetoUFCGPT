import functools
from dotenv import load_dotenv

from tools.eureca_cc_tools import *
from tools.resolucao_tools import *
from tools.guia_tools import *
from tools.web_search_tools import *
from prompts.cc_system_prompts import *
from .agent_class import *

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

'''EURECA_TOOLS = [
    get_calendario_recente,
    get_cursos_ativos, # testado
    get_curso, # testado
    get_curriculos, # testado
    get_disciplinas_curso, # testado
    get_disciplina, # testado
    get_plano_de_curso, # 
    get_plano_de_aulas, # 
    get_campi, # testado
    get_calendarios, # testado
    get_total_professores, # testado
    get_setores,
    get_estagios, #
    get_turmas, # testado (mais ou menos)
    get_media_notas_turma_disciplina # testado
]'''

CURSOS_EURECA_TOOLS = [
    get_cursos_ativos,
    get_curso,
    get_curriculos,
    get_curriculo_mais_recente,
    get_estudantes
]

DISCIPLINAS_EURECA_TOOLS = [
    get_disciplinas_curso,
    get_disciplina,
    get_plano_de_curso,
    get_plano_de_aulas,
    get_turmas,
    get_media_notas_turma_disciplina
]

CAMPI_EURECA_TOOLS = [
    get_campi,
    get_calendarios,
    get_calendario_recente
]

SETOR_PROFESSOR_ESTAGIO_TOOLS = [
    get_setores,
    get_total_professores,
    get_estagios
]

RESOLUCAO_TOOLS = [
    get_resolucao
]

ENROLLMENT_GUIDE_TOOLS = [
    get_guia_de_matriculas
]

NOTICES_TOOLS = [
    read_page
]

model = ChatOpenAI(model="gpt-3.5-turbo")

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

#eureca_agent = create_react_agent(model, tools=EURECA_TOOLS, state_modifier=EURECA_SYSTEM_PROMPT)
#eureca_node = functools.partial(agent_node, agent=eureca_agent, name="Agente_Eureca")

# Agente_Cursos_Eureca
cursos_eureca_agent = create_react_agent(model, tools=CURSOS_EURECA_TOOLS, state_modifier=CURSOS_SYSTEM_PROMPT)
cursos_eureca_node = functools.partial(agent_node, agent=cursos_eureca_agent, name="Agente_Cursos_Eureca")
# Agente_Disciplinas_Turmas_Eureca
disciplinas_eureca_agent = create_react_agent(model, tools=DISCIPLINAS_EURECA_TOOLS, state_modifier=DISCIPLINAS_TURMAS_SYSTEM_PROMPT)
disciplinas_eureca_node = functools.partial(agent_node, agent=disciplinas_eureca_agent, name="Agente_Disciplinas_Turmas_Eureca")
# Agente_Campus_Eureca
campus_eureca_agent = create_react_agent(model, tools=CAMPI_EURECA_TOOLS, state_modifier=CAMPI_SYSTEM_PROMPT)
campus_eureca_node = functools.partial(agent_node, agent=campus_eureca_agent, name="Agente_Campus_Eureca")
# Agente_Setor_Professor_Estagio_Eureca
set_prof_est_eureca_agent = create_react_agent(model, tools=SETOR_PROFESSOR_ESTAGIO_TOOLS, state_modifier=SETOR_PROFESSOR_ESTAGIO_SYSTEM_PROMPT)
set_prof_est_eureca_node = functools.partial(agent_node, agent=set_prof_est_eureca_agent, name="Agente_Setor_Professor_Estagio_Eureca")
# Agente_Resolucao
resolucao_agent = create_react_agent(model, tools=RESOLUCAO_TOOLS, state_modifier=RESOLUCAO_SYSTEM_PROMPT)
resolucao_node = functools.partial(agent_node, agent=resolucao_agent, name="Agente_Resolucao")
# Agente_Guia_Matriculas
enrollment_guide_agent = create_react_agent(model, tools=ENROLLMENT_GUIDE_TOOLS, state_modifier=ENROLLMENT_GUIDE_SYSTEM_PROMPT)
enrollment_guide_node = functools.partial(agent_node, agent=enrollment_guide_agent, name="Agente_Guia_Matriculas")
# Agente_Comunicados_Oficiais
official_notices_agent = create_react_agent(model, tools=NOTICES_TOOLS, state_modifier=OFFICIAL_NOTICES_SYSTEM_PROMPT)
official_notices_node = functools.partial(agent_node, agent=official_notices_agent, name="Agente_Comunicados_Oficiais")


def build_flow() -> StateGraph:
    """
    Constrói o grafo de estados
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("Agente_Supervisor", supervisor_agent)
    #workflow.add_node("Agente_Eureca", eureca_node)
    workflow.add_node("Agente_Cursos_Eureca", cursos_eureca_node)
    workflow.add_node("Agente_Disciplinas_Turmas_Eureca", disciplinas_eureca_node)
    workflow.add_node("Agente_Campus_Eureca", campus_eureca_node)
    workflow.add_node("Agente_Setor_Professor_Estagio_Eureca", set_prof_est_eureca_node)
    workflow.add_node("Agente_Resolucao", resolucao_node)
    workflow.add_node("Agente_Guia_Matriculas", enrollment_guide_node)
    workflow.add_node("Agente_Comunicados_Oficiais", official_notices_node)
    workflow.add_node("Agente_Sumarizador", output_summarizing_node)

    #workflow.add_edge("Agente_Eureca", "Agente_Supervisor")
    workflow.add_edge("Agente_Cursos_Eureca", "Agente_Supervisor")
    workflow.add_edge("Agente_Disciplinas_Turmas_Eureca", "Agente_Supervisor")
    workflow.add_edge("Agente_Campus_Eureca", "Agente_Supervisor")
    workflow.add_edge("Agente_Setor_Professor_Estagio_Eureca", "Agente_Supervisor")
    workflow.add_edge("Agente_Resolucao", "Agente_Supervisor")
    workflow.add_edge("Agente_Guia_Matriculas", "Agente_Supervisor")
    workflow.add_edge("Agente_Comunicados_Oficiais", "Agente_Supervisor")
    
    conditional_map = {
        "Agente_Cursos_Eureca": "Agente_Cursos_Eureca",
        "Agente_Disciplinas_Turmas_Eureca": "Agente_Disciplinas_Turmas_Eureca",
        "Agente_Campus_Eureca": "Agente_Campus_Eureca",
        "Agente_Setor_Professor_Estagio_Eureca": "Agente_Setor_Professor_Estagio_Eureca",
        "Agente_Resolucao": "Agente_Resolucao",
        "Agente_Guia_Matriculas": "Agente_Guia_Matriculas",
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