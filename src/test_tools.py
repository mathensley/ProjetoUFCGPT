from tools.web_search_tools import *
from tools_eureca import *
# print(read_page("https://www.prac.ufcg.edu.br/ultimas-noticias"))

base_url = "https://eureca.sti.ufcg.edu.br/das/v2"
course = "14102100"
#print(get_cursos(base_url))
#print(get_campi(base_url))

print(get_cursos_ativos(base_url))
