import operator

from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage
from pydantic import BaseModel

AGENTS = ["Agente_Cursos_Eureca", "Agente_Disciplinas_Turmas_Eureca", "Agente_Campus_Eureca", 
          "Agente_Setor_Professor_Estagio_Eureca", "Agente_Resolucao", "Agente_Guia_Matriculas", 
          "Agente_Localizacao", "Agente_Comunicados_Oficiais", "Agente_Sumarizador"]
OPTIONS = ("FINALIZAR",) + tuple(AGENTS)

class RouteResponse(BaseModel):
    next: Literal[OPTIONS]

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str