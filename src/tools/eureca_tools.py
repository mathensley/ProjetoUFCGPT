import requests
import json
from langchain_core.tools import tool

@tool
def get_cursos_ativos(base_url: str) -> list:
    """
    Buscar todos os cursos ativos da UFCG.
    
    Retorna uma lista de objetos JSON de curso. Cada um dos cursos retornados possuem essas informações:
    {
        codigo_do_curso: codigo do curso,
        descricao: nome do curso
    }
    """
    url_cursos = f'{base_url}/cursos'
    params = {
        'status-enum':'ATIVOS',
        'campus': '1'
    }
    response = requests.get(url_cursos, params=params)

    if response.status_code == 200:
        data_json = json.loads(response.text)
        return [{'codigo_do_curso': data['codigo_do_curso'], 'descricao': data['descricao']} for data in data_json]
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_curso(base_url: str, codigo_curso: str) -> list:
    """
    Descrição: Buscar informação de um curso da UFCG a partir do código do curso.
    """
    params = {
        'status-enum': 'ATIVOS',
        'curso': codigo_curso
    }
    url_cursos = f'{base_url}/cursos'
    response = requests.get(url_cursos, params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

@tool
def get_curriculos(base_url: str, codigo_curso: str) -> list:
    """
    Buscar todos os currículos de um curso, ou seja, a grade curricular do curso. 
    """
    response = requests.get(f'{base_url}/curriculos?curso={codigo_curso}')
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_disciplinas_curso(base_url: str, codigo_curso: str, codigo_curriculo: str) -> list:
    """
    Buscar todas as disciplinas de um curso.

    Retorna uma lista de disciplinas do curso. Cada uma das disciplinas possuem essas informações::
    {
        codigo_da_disciplina: Códido da disciplina,
        nome: Nome do curso
    }
    """
    params = {
        'curso': codigo_curso,
        'curriculo': codigo_curriculo
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        res = json.loads(response.text)
        return [{'codigo_da_disciplina': data['codigo_da_disciplina'], 'nome': data['nome']} for data in res]
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
def get_calendarios(base_url: str, campus: str) -> list:
    """
    Descrição: Buscar calendários da universidade. Ou seja, os periodos letivos que já ocorreram na UFCG até hoje.

    Returns:
    {
        campus: Código do campus, 
        descricao: Nome do campus,
        representacao: Número do campus em representação romana
    }
    """
    params = {
        'campus': campus
    }
    response = requests.get(f'{base_url}/calendarios', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_professores(base_url: str, setor: str) -> int:
    """
    Descrição: Busca a quantidade de professores de um centro.
    """
    params = {
        "status": "ATIVO",
        "setor": setor
    }
    response = requests.get(f'{base_url}/professores', params=params)

    if response.status_code == 200:
        return len(json.loads(response.text))
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