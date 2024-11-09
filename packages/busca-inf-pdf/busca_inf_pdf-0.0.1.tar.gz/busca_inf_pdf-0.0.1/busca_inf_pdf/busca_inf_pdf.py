# Tratamento dos dados
import pandas as pd
import numpy as np
# Regex para extração dos dados
import re
# Importação de PDF
import camelot
# Acesso as pastas
import os

import warnings
warnings.filterwarnings('ignore')


def busca_regex_pdf(pdf_path,
                        regex,
                        empresa:str=None,
                        mes:str = None):
    
    """
    Retorna todos os valores em que a escrita regex for verdadeira, a partir de um arquivo fornecido
    """
    # Definindo padrão da string CNPJ
    regex_cnpj = re.compile(regex)
    
    # Leitura das tabelas no PDF
    tables = camelot.read_pdf(pdf_path, pages="all")
    
    list_cnpj = []
    list_erro = []

    # Extraindo o nome do arquivo sem extensão
    nome_arquivo = str(pdf_path).split('\\')[-1].replace('.pdf', '')

    cnpj_encontrado = False
    for table in tables:
        # Convertendo tabela para uma lista de dicionários
        table_records = table.df.to_dict(orient='records')
        
        for row in table_records:
            for value in row.values():
                if regex_cnpj.search(value):
                    cnpj_encontrado = True
                    # Dividindo ocorrências para capturar CNPJs específicos em múltiplas linhas
                    ocorrencias = str(value).split('\n')
                    for ocorrencia in ocorrencias:
                        list_cnpj.append({
                            'Local Arquivo': pdf_path,
                            'Nome arquivo': nome_arquivo,
                            'informação': ocorrencia,
                            'Empresa':empresa,
                            'mes':mes
                        })
        
        # Caso nenhum CNPJ seja encontrado na tabela atual
        if cnpj_encontrado == False:
            list_erro.append({
                'Local Arquivo': pdf_path,
                'Nome arquivo': nome_arquivo,
                'informação': 'Não foi possível encontrar o CNPJ',
                'empresa': empresa,
                'mes':mes
            })

    return pd.DataFrame(list_cnpj), pd.DataFrame(list_erro)

def extract_regex_values(regex, string: str) -> str:
    """
    Retorna apenas o valor do regex fornecido
    """

    # Definindo padrão da string CNPJ
    regex_cnpj = re.compile(regex)
    
    # Encontrando todos os CNPJs no texto
    cnpj_list = re.findall(regex_cnpj, string)
    
    # Retornando como uma string, separada por vírgulas caso tenha múltiplos CNPJs
    return ', '.join(cnpj_list)


def notas_na_pasta(
                    path_arquivo, 
                    empresa=None,
                    mes:str = None):
    import os
    import pandas as pd

    """
    Calcula a quantidade de notas salvas em determinada pasta
    """

    caminhos = [os.path.join(path_arquivo, arquivo) for arquivo in os.listdir(path_arquivo)]
    nome_arquivo = [x.split('.pdf')[0] for x in os.listdir(path_arquivo) if x.endswith('.pdf')]
    empresa = [empresa] * len(caminhos) if empresa is not None else [None] * len(caminhos)
    mes = [mes] * len(caminhos) if mes is not None else [None] * len(caminhos)

    df = pd.DataFrame(
        {'Local Arquivo':caminhos,
        'Nome arquivo': nome_arquivo,
        'empresa': empresa,
        'mes':mes}
    )
    
    return df


def abertura_notas_e_criacao_lista(path_arquivos, str_regex: str, empresa=None, mes=None):
    
    """
    Cria uma lista com todas as notas que existem em uma determinada pasta
    """
    
    list_df = []
    list_ta_errado = []
    notas = []

    try:
        notas.append(notas_na_pasta(path_arquivo=path_arquivos, empresa=empresa, mes=mes))
    except:
        notas.append(
            pd.DataFrame(
                {'Local Arquivo':[path_arquivos],
                'Nome arquivo': [path_arquivos],
                'empresa': [empresa],
                'mes':[mes]}
    )         
        )

    for i in os.listdir(path_arquivos):
        caminho = os.path.join(path_arquivos, i)
        try:
            list_cnpj, list_erro =  busca_regex_pdf(caminho, 
                                                    str_regex= str_regex, 
                                                    empresa=empresa, 
                                                    mes=mes)

        except Exception as e:
            nome_arquivo = str(caminho).split('\\')[-1]
            nome_arquivo = nome_arquivo.split('.pdf')[0]

            list_erro = pd.DataFrame({'Local Arquivo': [path_arquivos],'Nome arquivo': [nome_arquivo],'informação':[ str(e)], 'empresa':empresa, 'mes':mes})

            list_ta_errado.append(list_erro)
            continue
            

        list_df.append(list_cnpj)

        if len(list_erro)>0:
            list_ta_errado.append(list_erro)
        else:
            continue

    return list_df, list_ta_errado, notas


def procura_desc_in_dict(dict: dict, 
                         term: str,
                         x: int,
                         y: int):
    """
    Verifica se um termo procurado na posição x de um dicionário é verdeiro, caso sim, busca o valor da posição y
    """
    if term in dict.get(x):
        produto = dict.get(y, "")
        return produto

    else:
        return False
    
def busca_no_dict_table(tables, term_loc: str, x:int, y: int):
    """
    A partir de uma table de pdf, converte em dict e busca o valor a partir da função 'procura_desc_in_dict'
    """
    produtos = []
    for table in tables:
        table_records = table.df.to_dict()
        for key, dict_pdf in table_records.items():
            if any(term_loc in str(value) for value in dict_pdf.values()):
                values = procura_desc_in_dict(dict_pdf, term_loc, x=x, y=y)
                if values:
                    return values
                else:
                    continue
            else:
                continue
    return 'Não foram encontrados produtos na nota'