import requests
import json
from langchain_core.tools import tool

@tool
def get_cursos_ativos(base_url: str) -> list:
    """
    Buscar todos os cursos ativos da UFCG.

    Args:
        base_url: URL base da API.
    
    Returns:
        Lista de cursos com 'codigo_do_curso' e 'descricao'.
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
def get_curso(base_url: str, codigo_do_curso: str) -> list:
    """
    Buscar informação de um curso da UFCG a partir do código do curso.

    Args:
        base_url: URL base da API.
        codigo_do_curso: código do curso.
    
    Returns:
        Lista com informações relevantes do curso específico.
    
    Nota:
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos`.
    """
    params = {
        'status-enum': 'ATIVOS',
        'curso': codigo_do_curso
    }
    url_cursos = f'{base_url}/cursos'
    response = requests.get(url_cursos, params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

@tool
def get_curriculos(base_url: str, codigo_do_curso: str) -> list:
    """
    Buscar todos os currículos de um curso, ou seja, a grade curricular do curso.

    Args:
        base_url: URL base da API.
        codigo_do_curso: código do curso.
    
    Returns:
        Lista com informações relevantes dos currículos do curso específico.
    
    Nota:
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos`.
    """
    response = requests.get(f'{base_url}/curriculos?curso={codigo_do_curso}')
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_disciplinas_curso(base_url: str, codigo_do_curso: str, codigo_curriculo: str) -> list:
    """
    Buscar todas as disciplinas de um curso.

    Args:
        base_url: URL base da API.
        codigo_do_curso: código do curso.
    
    Returns:
        Lista de disciplinas com 'codigo_da_disciplina' e 'nome'.
    
    Nota:
        Para usar este método, se o 'codigo_currículo' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_curriculos`.
    """
    params = {
        'curso': codigo_do_curso,
        'curriculo': codigo_curriculo
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        res = json.loads(response.text)
        return [{'codigo_da_disciplina': data['codigo_da_disciplina'], 'nome': data['nome']} for data in res]
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_plano_de_curso(base_url: str, codigo_disciplina: str, periodo: str) -> list:
    """
    Plano de curso de uma disciplina.

    Args:
        base_url: URL base da API.
        codigo_disciplina: código da disciplina.
        periodo: período letivo (calendário)
    
    Returns:
        Lista com informações relevantes do plano de curso de uma disciplina.
    
    Nota:
        Para usar este método, se o 'codigo_disciplina' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_disciplinas_curso`.
        Além disso, o 'periodo' deve ser informado pelo usuário, caso não seja fornecido, escolha o mais recente pelo método `get_calendarios`.
    """
    params = {
        'disciplina': codigo_disciplina,
        'periodo-de': periodo,
        'periodo-ate': periodo
    }

    response = requests.get(f'{base_url}/planos-de-curso', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

# Fazer método get_turmas()
@tool
def get_plano_de_aulas(base_url: str, codigo_disciplina: str, periodo: str, numero_turma: str) -> list:
    """
    Buscar plano de aulas de uma turma de uma disciplina.

    Args:
        base_url: URL base da API.
        codigo_disciplina: código da disciplina.
        periodo: período letivo (calendário).
        numero_turma: número da turma (e.g. 01, 02...).
    
    Returns:
        Lista com informações relevantes do plano de aulas da turma de uma disciplina.
    
    Nota:

    """
    params = {
        'disciplina': codigo_disciplina,
        'periodo-de': periodo,
        'periodo-ate': periodo,
        'turma': numero_turma
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

    Args:
        base_url: URL base da API.
    
    Returns:
        Lista com 'campus' (código do campus), 'descricao' (nome do campus) e 'representacao' (número do campus em romano).
    """
    response = requests.get(f'{base_url}/campi')

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_matriculas(base_url: str, codigo_do_curso: str, codigo_disciplina: str, turma: str, periodo: str) -> list:
    """
    Buscar matrículas dos alunos

    Args:

    Returns:

    """
    params = {
        'curso': codigo_do_curso,
        'disciplina': codigo_disciplina,
        'turma': turma,
        'periodo-de': periodo,
        'periodo-ate': periodo
    }

    response = requests.get(f'{base_url}/matriculas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_calendarios(base_url: str, campus: str) -> list:
    """
    Buscar calendários da universidade. Ou seja, os periodos letivos que já ocorreram na UFCG até hoje.

    Args:
        base_url: URL base da API.
        campus: código do campus.

    Returns:
        Lista com informações relevantes dos calendários acadêmicos do campus (como 'inicio_das_matriculas', 'inicio_das_aulas' e 'numero_de_semanas')
    
    Nota:
        Para usar este método, se o 'campus' (código do campus) não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_campi`.
    """
    params = {
        'campus': campus
    }
    response = requests.get(f'{base_url}/calendarios', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

# Fazer método get_setor()
@tool
def get_professores(base_url: str, setor: str) -> int:
    """
    Busca a quantidade de professores de um centro.

    Args:
        base_url: URL base da API.
        setor: 
    
    Returns:
        Um inteiro que representa o total de professores de um centro
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
    Buscar estágios.

    Args:

    Returns:
    
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