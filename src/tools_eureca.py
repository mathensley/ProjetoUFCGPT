import requests
import json
from langchain_core.tools import tool

@tool
def get_cursos(base_url):
    """
    Descrição: Buscar todos os cursos ativos da UFCG.
    
    Returns: Retorna uma lista de objetos JSON de curso. Cada um dos cursos retornados possuem essas informações:
    {
        codigo_do_curso: codigo do curso,
        descricao: nome do curso,
        status: ATIVO ou INATIVO,
        grau_do_curso: Como por exemplo, GRADUAÇÂO,
        codigo_do_setor: Codigo do setor,
        nome_do_setor: Nome do Centro a qual o curso pertence,
        campus: Código do Campus,
        nome_do_campus: Cidade do campus desse curso,
        turno: Integral ou noturno, matutino, vespertino, ...,
        periodo_de_inicio: Período de inicio do curso, ou seja quando foi criado (Por exemplo 1981.2 significa que o curso existe desde o período 2019.2),
        data_de_funcionamento: Data em que o curso foi criado em formato timestamp,
        codigo_inep: Valor inteiro do códido inep do Curso,
        modalidade_academica: BACHARELADO ou LICENCIATURA, ...,
        curriculo_atual: Ano em que o curriculo do curso mudou pela última vez (ou seja, inseriu ou removeu novas disciplinas da grade),
        area_de_retencao: Valor numérico entre 1 a 10 do onde o setor do curso se encontra,
        ciclo_enade: Valor numérico de quantos em quantos peridos o curso realiza o ENADE.
    }
    """
    url_cursos = f'{base_url}/cursos?status-enum=ATIVOS'
    response = requests.get(url_cursos)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

@tool
def get_curriculos(base_url, curso):
    """
    Descrição: Buscar todos os currículos de um curso, ou seja, a grade curricular do curso. 
    
    Returns: O curriculo tem essas informações. O curriculo retornado possui essas informações:
    {
        codigo_do_curso: Código do curso,
        codigo_do_curriculo: Ano em que o curriculo do curso mudou pela última vez (ou seja, inseriu ou removeu novas disciplinas da grade),
        regime: período em que o curriculo do curso mudou pela última vez (por exemplo, se o codigo_do_curriculo for 2010 e o regime for 2, então ele mudou em 2010.2),
        duracao_minima: Períodos mínimos que um estudante leva para se formar,
        duracao_maxima: Períodos máximos que um estudante pode ficar no curso,
        duracao_media: Número de períodos médio que um estudante leva para se formar,
        carga_horaria_creditos_minima: Restrição de créditos minimos que um estudante pode se matricular,
        carga_horaria_creditos_maxima: Restrição de créditos máximos que um estudante pode se matricular,
        carga_horaria_disciplinas_obrigatorias_minima: Número de horas mínimas de disciplinas obrigatórias que um estudante deve ter para se formar,
        carga_horaria_disciplinas_optativas_minima: Número de horas mínimas de disciplinas optativas que um estudante deve ter para se formar,
        carga_horaria_atividades_complementares_minima: Número de horas de atividades flexiveis que um estudante deve ter para poder se formar,
        carga_horaria_minima_total: Número de horas mínimas somadas entre disciplinas obrigatórias e optativas que leva um estudante a se formar,
        minimo_creditos_disciplinas_obrigatorias: Número de créditos mínimos de disciplinas obrigatórias que um estudante deve ter para se formar,
        minimo_creditos_disciplinas_optativas: Número de créditos mínimos de disciplinas optativas que um estudante deve ter para se formar,
        minimo_creditos_atividades_complementares: Número de horas créditos de atividades complementares que um estudante deve ter para se formar,
        minimo_creditos_total: Número de cŕeditos totais entre disciplinas obrigatórias, optativas e atividades complementares que um estudante deve ter para se formar,
        numero_disciplinas_obrigatorias_minimo: Quantidade minima de disciplinas obrigatórias que leva um estudante a se formar,
        numero_disciplinas_optativas_minimo: Quantidade máxima de disciplinas obrigatórias que leva um estudante a se formar,
        numero_atividades_complementares_minimo: Quantidade minima de atividades complementares que leva um estudante a se formar,
        numero_disciplinas_minimo: Número de disciplinas mínimo (soma das disciplinas obrigatórias e optativas) que leva um estudante a se formar,
        numero_interrupcoes_matricula_maximo: Número de vezes que um estudante pode trancar uma disciplina,
        numero_interrupcoes_periodo_maximo: Número de trancamento máximo total permitido pelo curso,
        numero_matriculas_institucionais_maximo: Número de vezes que um estudante pode se matricular no mesmo curso,
        numero_matriculas_extensao_maximo: None,
        carga_horaria_extensao: None,
        disciplina_atividades_complementares_flexiveis: Disciplinas de atividades complementares flexiveis,
        disciplina_atividades_complementares_extensao: Disciplinas de atividades complementares de extensão,
        periodo_inicio: None}
    """
    response = requests.get(f'{base_url}/curriculos?curso={curso}')
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

@tool
def get_disciplinas_curso(base_url, campus, curso, curriculo):
    """
    Descrição: Buscar todas as disciplinas de um curso.
    
    Returns: Retorna uma lista de disciplinas do curso. Cada uma das disciplinas possuem essas informações::
    {
        codigo_da_disciplina: Códido da disciplina,
        nome: Nome do curso,
        carga_horaria_teorica_semanal: Quantas horas teoricas tem uma disciplina no total,
        carga_horaria_pratica_semanal: Quantas horas praticas tem uma disciplina no total,
        quantidade_de_creditos: Quantos creéditos tem a disciplina,
        horas_totais: Quantas horas teoricas tem uma disciplina no total,
        media_de_aprovacao: Quantos alunos em média são aprovados nessa disciplina,
        carga_horaria_teorica_minima: Quantas horas teoricas mínimas pode ter a disciplina,
        carga_horaria_pratica_minima: Quantas horas praticas mínimas pode ter a disciplina,
        carga_horaria_teorica_maxima: Quantas horas teoricas máximas pode ter a disciplina,
        carga_horaria_pratica_maxima: Quantas horas práticas máximas pode ter a disciplina,
        numero_de_semanas: Quantas semanas tem essa disciplina (se por exemplo, for 10 então são 10 semanas de aula),
        codigo_do_setor: Código do setor a qual a disciplina pertence,
        nome_do_setor: Nome do setor a qual a disciplina pertencne,
        campus: Código do campus ao qual a disciplina pertence,
        nome_do_campus: Nome do campus ao qual a disciplina pertence,
        status: Status do curso, por exemplo ATIVO ou INATIVO,
        contabiliza_creditos: Informação sobre se contabiliza créditos com sim ou não,
        tipo_de_componente_curricular: Tipo de componente curricular,
        carga_horaria_extensao: Quantas horas de extensão a disciplina tem.
    }
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
        return None

@tool
def get_plano_de_curso(base_url, codigo_disciplina, periodo_de, periodo_ate):
    """
    Plano de curso de uma disciplina.
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
        return None

@tool
def get_plano_de_aulas(base_url, codigo_disciplina, periodo_de, periodo_ate):
    """
    Buscar plano de aulas de uma turma de uma disciplina com temas das aulas para cada dia de aula.
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
        return None

@tool
def get_campi(base_url):
    """
    Buscar todos os campi.
    """
    response = requests.get(f'{base_url}/campi')

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

@tool
def get_matriculas(base_url, curso, codigo_disciplina, turma, periodo_de, periodo_ate):
    """
    Buscar matrículas dos alunos numa turma de uma disciplina.
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
        return None

@tool
def get_calendarios(base_url):
    """
    Buscar calendários da universidade. Ou seja, os periodos letivos que já ocorreram na UFCG até hoje.
    """
    response = requests.get(f'{base_url}/calendarios')

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

@tool
def get_professores(base_url, setor):
    """
    Buscar professores de um centro.
    """
    params = {
        "status": "ATIVO",
        "setor": setor
    }
    response = requests.get(f'{base_url}/professores', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

@tool
def get_estagios(base_url, inicio_de, fim_ate, unidade):
    """
    Buscar estágios dos estudantes por unidade acadêmica.
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
        return None