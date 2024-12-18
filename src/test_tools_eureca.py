import requests
import json
import numpy as np

def get_cursos_ativos(base_url: str) -> list:
    """
    Descrição: Buscar todos os cursos ativos da UFCG.
    
    Returns: Retorna uma lista de objetos JSON de curso. Cada um dos cursos retornados possuem essas informações:
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
        return [{
            'codigo_do_curso': data['codigo_do_curso'], 
            'descricao': data['descricao']} 
            for data in data_json
        ]
    else:
        return None


def get_curso(base_url: str, course: str):
    """
    Descrição: Buscar informação de um curso da UFCG a partir do código do curso.
    
    Returns: Retorna um objeto JSON de curso. As informações retornadas são:
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
    
    params = {
        'status-enum': 'ATIVOS',
        'curso': course
    }
    url_cursos = f'{base_url}/cursos'
    response = requests.get(url_cursos, params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None


def get_curriculos(base_url: str, curso: str, curriculo: str) -> list:
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
        periodo_inicio: Período de início
    }
    """
    
    params = {
        'curso': curso,
        'curriculo': curriculo
    }
    response = requests.get(f'{base_url}/curriculos', params=params)
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None


def get_disciplinas_curso(base_url, curso, curriculo):
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
        'campus': '01',
        'curso': curso,
        'curriculo': curriculo
    }
    response = requests.get(f'{base_url}/disciplinas', params=params)

    if response.status_code == 200:
        res = json.loads(response.text)
        return [{'codigo_da_disciplina': data['codigo_da_disciplina'], 'nome': data['nome']} for data in res]
    else:
        return None


def get_plano_de_curso(base_url, codigo_disciplina, periodo_de, periodo_ate):
    """
    Descrição: Plano de curso de uma disciplina.
    
    Returns: Retorna o plano de curso de uma disciplina. As informações retornadas são:
    {
        turma: Código da turma,
        codigo_da_disciplina: Código da disciplina,
        nome_da_disciplina: Nome da disciplina,
        codigo_do_setor: Código do setor ao qual a curso pertence,
        nome_do_setor: Nome do setor ao qual o curso pertence,
        periodo: Perído em que a disciplina foi dada,
        ementa: Descrição da ementa do curso. Ou seja, o que é ensinado nessa disciplina e suas metodologias de ensino.
    }
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


def get_plano_de_aulas(base_url, codigo_disciplina, periodo_de, periodo_ate):
    """
    Descrição: Buscar plano de aulas de uma turma de uma disciplina com temas das aulas para cada dia de aula.
    
    Returns: Retorna uma lista de plano de aulas. Cada plano de aula tem essas informações: 
    {
        turma: Código da turma,
        codigo_da_disciplina: Código da disciplina,
        periodo: Período da disciplina,
        aula_sequencia: Numero de aulas necessarios para o conteudo,
        data: Data em que o conteudo será ensinado,
        horas: Horas de aulas necessárias,
        assunto: Descrição do plano da aula que será realizado.
    },
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


def get_campi(base_url):
    """
    Descrição: Buscar todos os campi. 
    
    Returns: Retorna uma lista de objetos JSON com as informações retornadas são: 
    {
        campus: Código do campus, 
        descricao: Nome do campus,
        representacao: Número do campus em representação romana
    }
    """
    response = requests.get(f'{base_url}/campi')

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None


def get_matriculas(base_url, curso, codigo_disciplina, turma, periodo_de, periodo_ate):
    """
    Descrição: Buscar matrículas dos alunos numa turma de uma disciplina.
    
    Returns: Retorna uma lista de matriculas de estudantes em uma disciplina. Cada informação tem: 
    {
        matricula_do_estudante: Matrícula do estudante,
        codigo_da_disciplina: Código da disciplina cursada,
        nome_da_disciplina: Nome da disciplina,
        periodo: Período em que está o estudante começou a cursar a disciplina,
        turma: Número da turma,
        status: Status da matrícula do estudante,
        tipo: Tipo de disciplina,
        media_final: Média final do aluno matriculado,
        dispensas: Caso haja dispensa, ele informa como ele passou na disciplina com a dispensa.
    }
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


def get_calendarios(base_url, campus):
    """
    Descrição: Buscar calendários da universidade. Ou seja, os periodos letivos que já ocorreram na UFCG até hoje.
    
    Returns: Retorna uma lista de calendários (períodos) que a UFCG já teve desde 2004 até hoje. Cada calendário tem essas informações:
    {
        id: Código do calendário,
        periodo: Período em que o calendário foi iniciado,
        campus: Código do campus,
        inicio_das_matriculas: Timestamp de inicio da matricula dos estudantes,
        inicio_das_aulas: Timestamp do inicio das aulas,
        um_terco_do_periodo: Um terço do período (data limite de trancamento de algum(as) disciplina(s)),
        ultimo_dia_para_registro_de_notas: Ultimo dia de aula,
        um_quarto_do_periodo: Timestamp de um quarto do período,
        numero_de_semanas: Número de semanas de aula
    }
    """
    params = {
        'campus': campus
    }
    response = requests.get(f'{base_url}/calendarios', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None









# Sem tools
def get_professores(base_url, setor):
    """
    Descrição: Busca a quantidade de professores de um centro.
    
    Returns: Retorna a quantidade de professores do centro.
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


# Com tools
def get_setores(base_url, campus):
    params = {
        "campus": campus
    }
    response = requests.get(f'{base_url}/setores', params=params)

    if response.status_code == 200:
      return json.loads(response.text)
    else:
      return None


# Sem tools
def get_total_professores(base_url, setor):
    """
    Descrição: Busca a quantidade de professores de um centro.
    
    Returns: Retorna a quantidade de professores do centro.
    """
    params = {
        "status": "ATIVO",
        "setor": setor
    }
    response = requests.get(f'{base_url}/professores', params=params)

    if response.status_code == 200:
        return len(json.loads(response.text))
    else:
        return None


# Sem tools
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


# Com tools
def get_estagios(base_url, inicio_de, fim_ate, setor):
    """
    Descrição: Buscar estágios dos estudantes por setor.
    
    Returns: Retorna as informações dos estágios dos estudantes de um setor. Cada obeto retornado tem: 
    {
        id: Id do estágio,
        matricula_do_estudante: Matricula do estudante,
        id_concedente: Id do concedente,
        uf_concedente: Sigla da unidade federativa do estágio,
        matricula_do_docente: matricula do docente orientador do estagio,
        departamento: Nome do departamento,
        nome_docente: Nome do docente,
        obrigatorio: True ou False,
        inicio_vigencia: Timestamp,
        final_vigencia: Timestamp,
        carga_semanal: Numero de horas trabalhadas semanalmente,
        status: Status do estágio,
        codigo_da_disciplina: código da disciplina de estágio,
        agente_integracao: None,
        bolsa_mensal: Valor da bolsa,
        auxilio_transporte_diario: Valor do auxílio transporte
    }
    """
    params = {
        "inicio-de": inicio_de,
        "fim-ate": fim_ate,
    }

    response = requests.get(f'{base_url}/estagios', params=params)

    if response.status_code == 200:
        estagiarios = json.loads(response.text)
        professores = get_professores(base_url, setor)
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
        return None

def get_turmas(base_url, periodo, disciplina):
    params = {
        "periodo-de": periodo,
        "periodo-ate": periodo,
        "disciplina": disciplina
    }
    
    response = requests.get(f'{base_url}/turmas', params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
      return None

def get_estudantes_matriculados(base_url, periodo, disciplina, turma):
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
      return None



def get_estudantes_formados(base_url, codigo_curso, periodo):
    params = {
        "curso": codigo_curso,
        "situacao-do-estudante": "EGRESSOS",
        "periodo-de-evasao-de": periodo,
        "periodo-de-evasao-ate": periodo
    }

    response = requests.get(f'{base_url}/estudantes', params=params)

    if response.status_code == 200:
        return len(json.loads(response.text))

def get_horarios_disciplinas(base_url, disciplina, turma, periodo):
    params = {
        "disciplina": disciplina,
        "turma": turma,
        "periodo-de": periodo,
        "periodo-ate": periodo
    }

    response = requests.get(f'{base_url}/horarios', params=params)

    if response.status_code == 200:
        horarios = json.loads(response.text)
        
        
        filtros_horarios = []
        turmas_map = {}

        for horario in horarios:
            turma = horario['turma']
            sala = horario['codigo_da_sala']
            dia = str(horario['dia'])
            horario_formatado = f"{horario['hora_de_inicio']}h às {horario['hora_de_termino']}h"

            if turma not in turmas_map:
                turmas_map[turma] = {
                    'turma': turma,
                    'sala': sala,
                    'horarios': {}
                }
                filtros_horarios.append(turmas_map[turma])

            turmas_map[turma]['horarios'][dia] = horario_formatado

        return filtros_horarios


def get_disciplina(base_url, disciplina):
  params = {
    'disciplina': disciplina,
  }

  response = requests.get(f'{base_url}/disciplinas', params=params)

  if response.status_code == 200:
    return json.loads(response.text)
  else:
    return None

def pre_requisitos_disciplinas(base_url, disciplina, curriculo):
    params = {
        'disciplina': disciplina,
        'curriculo': curriculo
    }

    response = requests.get(f'{base_url}/pre-requisito-disciplinas', params=params)

    if response.status_code == 200:
        requisitos = json.loads(response.text)
        disciplinas = []

        for requisito in requisitos:
            disciplina_req = get_disciplina(
                base_url,
                requisito['condicao'],
            )

            disciplinas.append(disciplina_req[0]['nome'])

        return set(disciplinas)
    
