from tools.web_search_tools import *
from test_tools_eureca import *
# print(read_page("https://www.prac.ufcg.edu.br/ultimas-noticias"))

base_url = "https://eureca.sti.ufcg.edu.br/das/v2"
course = "14102100"
#print(get_cursos(base_url))
#print(get_campi(base_url))

print(get_estagios(base_url, '2024', '2024', '14110000'))