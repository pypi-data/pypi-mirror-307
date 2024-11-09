# BUSCA INFORMAÇÃO NO PDF
## Objetivo

Pacote desenvolvido para auxiliar na busca de informações contidas nos pdf, o pacote opera na busca de duas maneiras;
1. Busca por Regex: Nas fuções que utilizam a busca por regex os códigos foram desenvolvidos para buscar em todos os valores existentes no pdf, isto pode tornar mais lenta a leitura.
2. Busca por posição: Na busca por posição, é necessário informar o termo que se busca e o local que ele se encontra, mais a frente serão demonstrados exemplos.

## Funções

### Instalação 
    ```bash 
    pip install busca_inf_pdf
    ```




### busca_regex_pdf
   1. Esta função busca em um dicionário o texto em regex informado e retorna o valor conforme pesquisado, recebe os seguintes argumentos:
      1. pdf_path (obrigatório): Caminho em que se encontra o arquivo pdf
      2. regex (obrigatório): Código regex que deseja buscar
      3. empresa (opcional): Nome da empresa, se não informar será atribuido como None
      4. mes (opcional): Mês de referência, se não informar será atribuido como None
   
      #### Exemplo
      ```python
        import busca_inf_pdf as bid

        path = r'./arquivo.pdf'
        regex = r'\d{2}\.\d{3}\.\d{3}/0001-\d{2}'
        empresa = 'Python Inc'
        mes = 'Janeiro'

        bid.busca_regex_pdf(path=path,
                                regex=regex,
                                empresa = empresa,
                                mes=mes)

### extract_regex_values
   1. Esta função extrai apenas o valor regex buscado e recebe os seguintes argumentos:
      1. regex (obrigatório): Informa o código regex que será buscado
      2. string (obrigatório): Informar a string que contém o dado

      #### Exemplo
      ```python
        import busca_inf_pdf as bid

        regex = r'\d{2}\.\d{3}\.\d{3}/0001-\d{2}'
        string  = 'CNPJ: 09.157.003/0001-37'
       

        bid.extract_regex_values(
            regex = regex,
            sting = string
        )

### abertura_notas_e_criacao_lista
   1. Esta função busca em um diretório todos os arquivos pdf e realiza a extração dos dados, retonando duas listas, uma com os arquivos que deram erro e outra com o valor procurado:
      1. path_arquivos (obrigatório): Caminho da pasta com os arquivos
      2. str_regex (obrigatório): Código regex que deseja buscar
      3. empresa (opcional): Nome da empresa, se não informar será atribuido como None
      4. mes (opcional): Mês de referência, se não informar será atribuido como None

      #### Exemplo
      ```python
        import busca_inf_pdf as bid
        import os

        list_pdf = os.listdir('diretorio com os arquivos pdf')
        regex = r'\d{2}\.\d{3}\.\d{3}/0001-\d{2}'
        empresa = 'Python Inc'
        mes = 'Janeiro'
       

        bid.abertura_notas_e_criacao_lista(path_arquivos=list_pdf,
                                regex=regex,
                                empresa = empresa,
                                mes=mes)

### procura_desc_in_dict
   1. Esta função busca em uma lista se determinado termo esta na posição x e retorna a posição y, os argumentos são:
      1. dict: dict (obrigatório): Dicioário que deseja avaliar
      2. term: str (obrigatório): Palavra que busca para retorno
      3. x: int (obrigatório): Posição em que a palavra buscada no dicionário deve estar
      4. y: int (obrigatório): Posição em que a palavra de retorno deve estar

      #### Exemplo
      ```python
        import busca_inf_pdf as bid
        import os

        bid.procura_desc_in_dict(
            dict = dicionario_a_partir_pdf,
            term = 'DESCR',
            x=0,
            y=1
        )

### busca_no_dict_table
   1. Esta função busca em uma lista se determinado termo esta na posição x e retorna a posição y, os argumentos são:
      1. tables (obrigatório): retorno ao abrir um pdf utilizando camelot
      2. term_loc: str (obrigatório): Palavra que busca para retorno
      3. x: int (obrigatório): Posição em que a palavra buscada no dicionário deve estar
      4. y: int (obrigatório): Posição em que a palavra de retorno deve estar


      #### Exemplo
      ```python
        import busca_inf_pdf as bid
        import camelot

        tables = camelot.read_pdf('arquivo.pdf', pages="all")

        bid.busca_no_dict_table(
            tables = tables,
            term = 'DESCR',
            x=0,
            y=1
        )