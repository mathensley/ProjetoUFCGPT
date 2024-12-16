import requests
import numpy as np
import json
from langchain_core.tools import tool

# Testado
# Teste1: Quantos professores tem na unidade academica de letras?                           Resp: A Unidade Acadêmica de Letras possui 67 professores.
# Teste2: Quantos professores tem no CEEI - CENTRO DE ENGENHARIA ELÉTRICA E INFORMÁTICA?    Resp: Não foi possível obter a quantidade de professores no CEEI - CENTRO DE ENGENHARIA ELÉTRICA E INFORMÁTICA, pois os professores pertencem às unidades acadêmicas específicas. Por favor, informe a unidade acadêmica desejada para obter essa informação.
# Quantos professores tem na UFCG? 1684.
@tool
def get_total_professores(base_url: str, setor_unidade: str) -> int:
    """
    Busca a quantidade total de professores de um setor (unidade).

    Args:
        base_url: URL base da API.
        setor_unidade: 'código_setor' (unidade) do campus.
    
    Returns:
        Um inteiro que representa o total de professores de um setor (unidade).
    
    Nota:
        Para usar este método, se o 'setor_unidade' (código do setor) não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_setores` baseado no nome da unidade fornecido pelo usuário.
        Se o nome da unidade não tiver sido informado, e tiver sido informado 'UFCG' use uma string vazia como entrada para 'setor_unidade'.
    """
    params = {
        "status": "ATIVO",
        "setor": setor_unidade
    }
    response = requests.get(f'{base_url}/professores', params=params)

    if response.status_code == 200:
        return len(json.loads(response.text))
    else:
        return [{"erro": "Não foi possível obter a informação (possível causa: \nProfessores pertencem as unidades. Por favor, informe a unidade acadêmica.)."}]


# Testado
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


# Testado.
# Teste1: Me de as informacoes do curso de letras frances. Resp: Resposta correta.
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


# Testado.
# Teste1: Qual o curriculo mais recente do curso de ciencia da computacao. Resp.: Código do currículo: 2023
# Teste2: Quais são todos os curriculos do curso de ciencia da computacao? Resp.: 1. Currículo de código 1979, 2. Currículo de código 1990, 3. Currículo de código 1999, 4. Currículo de código 2017, 5. Currículo de código 2023
# Teste3: Qual o curriculo mais recente do curso de engenharia civil? Resp.: 
#           O currículo mais recente do curso de Engenharia Civil é o de 2014, que possui as seguintes características:- Código do Currículo: 2014
#           - Regime: 1
#           - Duração Mínima: 10 semestres
#           - Duração Máxima: 15 semestres
#           - Carga Horária Mínima Total: 3660 horas
#           - Número Mínimo de Disciplinas Obrigatórias: 54
#           - Número Mínimo de Disciplinas Optativas: 4
#           - Número Mínimo de Atividades Complementares: 4
#           - Número Mínimo de Disciplinas: 62
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
        Para usar este método, se o 'codigo_do_curso' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_cursos_ativos` e recuperar o código do curso.
        Se a pergunta for o curriculo mais recente e tiver apenas um curriculo, traga as informações desse único curriculo como resposta.
    """
    response = requests.get(f'{base_url}/curriculos?curso={codigo_do_curso}')
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

# FAZER TESTE
@tool
def get_disciplinas_curso(base_url: str, codigo_do_curso: str, codigo_curriculo: str) -> list:
    """
    Buscar todas as disciplinas de um curso.

    Args:
        base_url: URL base da API.
        codigo_do_curso: código do curso.
        codigo_curriculo: código do currículo
    
    Returns:
        Lista de disciplinas com 'codigo_da_disciplina' e 'nome'.
    
    Nota:
        Para usar este método, se o 'codigo_currículo' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_curriculos`.
    """
    params = {
        'campus': '01',
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
def get_disciplina(base_url: str, codigo_do_curso: str, codigo_curriculo: str, codigo_da_disciplina: str) -> list:
    """
    Buscar as informações de uma disciplina.

    Args:
        base_url: URL base da API.
        codigo_do_curso: código do curso.
        codigo_curriculo: código do currículo
        codigo_da_disciplina: código da disciplina específica.
    
    Returns:
        Lista com informações relevantes sobre uma disciplica específica.
    
    Nota:
        Para usar este método, se todos os parâmetros não tiverem sido informados pelo usuário, obtenha os parâmetros previamente com a tool `get_disciplinas_curso`.
    """
    params = {
        'campus': '01',
        'curso': codigo_do_curso,
        'curriculo': codigo_curriculo,
        'disciplina': codigo_da_disciplina
    }

    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
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


def get_professores(base_url: str, setor_centro: str) -> list:
    """
    Busca as informações de professores de um setor (centro).
    
    Args:
        base_url: URL base da API.
        setor_centro: 'código_setor' (centro) do campus.

    Returns:
        Lista com as informações relevantes de professores de um setor (centro).
    """
    params = {
        "status": "ATIVO",
        "setor": setor_centro
    }
    response = requests.get(f'{base_url}/professores', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_setores(base_url: str) -> list:
    """
    Busca as informações de setor (centro) do campus da UFCG.

    Args:
        base_url: URL base da API.
    
    Returns:
        Lista com informações relevantes do setor (centro) específico.
    """
    params = {
        "campus": '1'
    }
    response = requests.get(f'{base_url}/setores', params=params)

    if response.status_code == 200:
      return json.loads(response.text)
    else:
      return [{"erro": "Não foi possível obter informação da UFCG."}]

def extrair_insights_estagios(estagiarios, uf):
    estagiarios_uf = ([
        est for est in estagiarios
        if (est['uf_concedente'] == uf)
    ])
  
    bolsas = [
        float(estagiario['bolsa_mensal']) if estagiario['bolsa_mensal'] is not None else 0 
        for estagiario in estagiarios_uf
    ]
    auxilio_transporte = [
        float(estagiario['auxilio_transporte_diario']) if estagiario['auxilio_transporte_diario'] is not None else 0 
        for estagiario in estagiarios_uf
    ]

    return {
        "total_estagiarios": len(estagiarios_uf),
        "bolsa_mensal_minima": float(f'{min(bolsas):.2f}'),
        "bolsa_mensal_maxima": float(f'{max(bolsas):.2f}'),
        "bolsa_mensal_media": float(f'{np.mean(bolsas):.2f}'),
        "auxilio_transporte_diario_minimo": float(f'{min(auxilio_transporte):.2f}'),
        "auxilio_transporte_diario_maximo": float(f'{max(auxilio_transporte):.2f}'),
        "auxilio_transporte_diario_medio": float(f'{np.mean(auxilio_transporte):.2f}')
    }

@tool
def get_estagios(base_url: str, ano: str, setor_centro_unidade: str) -> list:
    """
    Buscar informações sobre estágios.

    Args:
        base_url: URL base da API.
        ano: ano de estágio.
        setor_centro_unidade: 'código_setor' (centro ou unidade) do campus.
    
    Returns:
        Lista com informações relevantes de estágio.
    
    Nota:
        Para usar este método, se o 'setor_centro_unidade' (código do setor) não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_setores` baseado no nome do centro ou unidade fornecido pelo usuário.
        Da mesma forma, caso o ano de estágio não tiver sido informado pelo usuário, escolha o ano mais recente.
    """
    params = {
        "inicio-de": ano,
        "fim-ate": ano
    }

    response = requests.get(f'{base_url}/estagios', params=params)

    if response.status_code == 200:
        estagiarios = json.loads(response.text)
        professores = get_professores(base_url, setor_centro_unidade)
        professores = [professor['matricula_do_docente'] for professor  in professores]

        estagiarios_unidade = [
            estagiario for estagiario in estagiarios
            if (estagiario['matricula_do_docente'] in professores)
        ]
        estados = list({estagiario['uf_concedente'] for estagiario in estagiarios_unidade})
        estados_res = {}
        for uf in estados:
            estados_res[uf] = extrair_insights_estagios(estagiarios=estagiarios_unidade, uf=uf)
        return estados_res
    else:
        return [{"erro": "Não foi possível obter informação da UFCG."}]

@tool
def get_turmas(base_url: str, periodo: str, disciplina: str) -> list:
    """
    Buscar turmas.

    Args:
        base_url: URL base da API.
        periodo: o período em que a turma está.
        disciplina: a disciplina que a turma está.
    
    Returns:
        Lista com informações relevantes das turmas.
    
    Nota:
        Para usar este método, se o 'periodo' não tiver sido informado pelo usuário, ele deve ser obtido previamente por `get_calendarios` e deve ser o último objeto da lista (o período mais recente).
        Além disso, se a disciplina (código da disciplina) não for informado, porém o nome da disciplina e o nome do curso tiver sido informado, busque o curso em `get_cursos` e adisciplina desejada em `get_disciplinas_curso`
    """
    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "disciplina": disciplina
    }
    
    response = requests.get(f'{base_url}/turmas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
      return [{"erro": "Não foi possível obter informação da UFCG."}]

def get_media_notas_turma_disciplina(base_url: str, periodo: str, disciplina: str, turma: str) -> dict:
    """
    Buscar as notas de estudantes em uma turma de uma disciplina.

    Args:
        base_url: URL base da API.
        periodo: o período em que a turma está.
        disciplina: a disciplina que a turma está.
        turma: a turma em questão.
    
    Returns:
        Dicionário com o intervalo das médias das notas de dada disciplina de uma turma.
    
    Nota:
        Para usar este método, se a 'turma' não tiver sido informada pelo usuário, use a turma '01'.
    """
    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "disciplina": disciplina,
        "turma": turma
    }

    response = requests.get(f'{base_url}/matriculas', params=params)

    if response.status_code == 200:
        matriculas = json.loads(response.text)
        
        medias = [
            matricula["media_final"] 
            if matricula["media_final"] is not None else 0
            for matricula in matriculas
        ]
        return {
            "medias_menores_que_5": 
            len([media for media in medias if float(media) < 5]),
            "medias_maior_ou_igual_a_5.0_e_menor_que_7.0": 
            len([media for media in medias if float(media) >= 5 and float(media) < 7]),
            "medias_maior_ou_igual_a_7.0_e_menor_que_8.5": 
            len([media for media in medias if float(media) >= 7 and float(media) < 8.5]),
            "medias_maior_ou_igual_a_8.5_e_menor_ou_igual_a_10": 
            len([media for media in medias if float(media) >= 8.5 and float(media) <= 10])
        }
    else:
      return [{"erro": "Não foi possível obter informação da UFCG."}]