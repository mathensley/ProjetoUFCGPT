import requests
import json
from langchain_core.tools import tool

@tool
def get_cursos(base_url: str) -> list:
    """
    Buscar todos os cursos da UFCG
    """
    url_cursos = f'{base_url}/cursos?status-enum=ATIVOS'
    response = requests.get(url_cursos)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_curriculos(base_url: str, curso: str) -> list:
    """
    Buscar todos os currículos de um curso
    """    
    response = requests.get(f'{base_url}/curriculos?curso={curso}')
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_disciplinas_curso(base_url: str, campus: str, curso: str, curriculo: str) -> list:
    """
    Buscar todas as disciplinas de um curso
    """
    params = {
        'campus': campus,
        'curso': curso,
        'curriculo': curriculo
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_plano_de_curso(base_url: str, codigo_disciplina: str, 
                       periodo_de: str, periodo_ate: str) -> list:
    """
    Plano de curso de uma disciplina
    """
    params = {
        'disciplina': codigo_disciplina,
        'periodo-de': periodo_de,
        'periodo-ate': periodo_ate
    }

    response = requests.get(f'{base_url}/planos-de-curso', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_plano_de_aulas(base_url: str, codigo_disciplina: str, 
                       periodo_de: str, periodo_ate: str) -> list:
    """
    Buscar plano de aulas de uma turma de uma disciplina
    """
    params = {
        'disciplina': codigo_disciplina,
        'periodo-de': periodo_de,
        'periodo-ate': periodo_ate
    }

    response = requests.get(f'{base_url}/aulas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_campi(base_url: str) -> list:
    """
    Buscar todos os campi
    """
    response = requests.get(f'{base_url}/campi')

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_matriculas(base_url: str, curso: str, 
                   codigo_disciplina: str, turma: str, periodo_de: str, periodo_ate: str) -> list:
    """
    Buscar matrículas dos alunos
    """
    params = {
        'curso': curso,
        'disciplina': codigo_disciplina,
        'turma': turma,
        'periodo-de': periodo_de,
        'periodo-ate': periodo_ate
    }

    response = requests.get(f'{base_url}/matriculas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_calendarios(base_url: str) -> list:
    """
    Buscar calendários da universidade
    """
    response = requests.get(f'{base_url}/calendarios')

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_professores(base_url: str, setor: str) -> list:
    """
    Buscar professores
    """
    params = {
        "status": "ATIVO",
        "setor": setor
    }
    response = requests.get(f'{base_url}/professores', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_estagios(base_url: str, inicio_de: str, fim_ate: str, unidade: str) -> list:
    """
    Buscar estágios
    """
    params = {
        "inicio-de": inicio_de,
        "fim-ate": fim_ate,
    }
    
    response = requests.get(f'{base_url}/estagios', params=params)

    if response.status_code == 200:
        estagiarios = json.loads(response.text)

        professores = get_professores(unidade)

        estagiarios_unidade = [
            estagiario for estagiario in estagiarios
            if any(professor['matricula_do_docente'] == estagiario['matricula_do_docente'] for professor in professores)]
        return estagiarios_unidade
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]