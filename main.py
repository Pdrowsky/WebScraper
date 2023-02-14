from urllib.request import urlopen
import re

class Dia:
    def __init__(self, dia: str, precipitacao: str, molhamento_foliar: str, temp_med_ar: str, temp_min_ar: str,
                 temp_max_ar: str, umidade_relativa_med: str, mes: str, ano: str):
        self.dia = dia
        self.precipitacao = precipitacao
        self.molhamento_foliar = molhamento_foliar
        self.temp_med_ar = temp_med_ar
        self.temp_min_ar = temp_min_ar
        self.temp_max_ar = temp_max_ar
        self.umidade_relativa_med = umidade_relativa_med
        self.mes = mes
        self.ano = ano

#FEITO (lista de todas as URLs a serem extraídas)
lista_urls = [
    "https://ciram.epagri.sc.gov.br/agroconnect/busca-outros-produtos.jsp?cd_estacao=2423&cd_cultura=0&produto=resumos_diarios&cd_variavel=192&WS=687&HS=633&grupo=0&data=03-02-2022&nhoras=1&dt=1675433206522&date=43696800&idestacao=Bom%20Retiro%20-%20Jo%C3%A3o%20Paulo:%202423&ka=16754332#"
              #,"https://ciram.epagri.sc.gov.br/agroconnect/busca-outros-produtos.jsp?cd_estacao=2386&cd_cultura=0&produto=resumos_diarios&cd_variavel=192&WS=687&HS=633&grupo=0&data=03-02-2023&nhoras=1&dt=1675433742164&date=43696800&idestacao=Presidente%20Get%C3%BAlio%20-%20Serra%20dos%20%C3%8Dndios:%202386&ka=16754337"
              ]


todos_os_dias = [] #Armazenamento dos objetos a serem transcritos para xlsx ou database.

for url in lista_urls:
    #FEITO (abrir a url)
    pagina = urlopen(url)
    html_bytes = pagina.read()
    html_fim = html_bytes.decode('utf-8')

    #FEITO (pegar o título)
    index_inicio_titulo = html_fim.find('<b><H6>') + len('<b><H6>')
    index_fim_titulo = html_fim.find('</b></H6>')
    titulo = html_fim[index_inicio_titulo:index_fim_titulo]

    #FEITO (pegar o mês e o ano)
    mes = titulo[len(titulo)-8:len(titulo)-5]
    ano = titulo[len(titulo)-4:]

    #FEITO (excluir tudo até o título)
    html_fim = html_fim[index_fim_titulo+len('</b></H6>'):]

    #FEITO (extrair cabeçalho da tabela)
    html_heading = html_fim
    cabecalho = []
    while len(html_heading) > 1000:
        try:
            pattern = "<th.*?>.*?</th.*?>"
            match_results = re.search(pattern, html_heading)
            conteudo_tabela = re.sub('<.*?>', '', match_results.group())
            html_heading = html_heading[html_heading.find(match_results.group())+len(match_results.group()):]
            cabecalho.append(conteudo_tabela)
        except Exception:
            pass
    cabecalho = cabecalho[0:cabecalho.index('Totais')]
    dias = cabecalho[cabecalho.index('01'):]
    legenda = cabecalho[0:cabecalho.index('01')]

    #FEITO (extrair resultados da tabela)
    html_resultados = html_fim
    resultados = []
    while len(html_resultados) > 1000:
        try:
            pattern = "<td.*?>.*?</td.*?>"
            match_results = re.search(pattern, html_resultados)
            conteudo_tabela = re.sub('<.*?>','',match_results.group())
            html_resultados = html_resultados[html_resultados.find(match_results.group())+len(match_results.group()):]
            resultados.append(conteudo_tabela)
        except Exception:
            pass
    resultados = resultados[0:resultados.index('')]

    #FEITO (cria objetos para cada dia com todas as suas informações)
    result_count = 0
    conjunto_dias = []
    for dia in dias:
        data = Dia(dia, resultados[result_count], resultados[result_count+1], resultados[result_count+2],
                   resultados[result_count+3], resultados[result_count+4], resultados[result_count+5], mes, ano)
        result_count += 6
        conjunto_dias.append(data)

    #FEITO (salva os dias do mês no total de dias)
    todos_os_dias += conjunto_dias