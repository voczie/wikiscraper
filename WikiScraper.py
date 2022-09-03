##############################################################################
###  - Nome do Programa:   WikiScrapper                                    ###
###  - Objetivo:           Web Scrapper (Expressões Regulares)             ###
###  - Autores:            Alexandre Bezerra de Lima                       ###
###                        Maria Victória Grisi                            ###
###  - Data de Início:     14/06/2021                                      ###
###  - Data de Término:    01/07/2021                                      ###
###  - GitHub:             https://github.com/voczie/wikiscrapper          ###
##############################################################################



### Importando as bibliotecas ###

import re
from sre_constants import ANY_ALL
import requests
from requests.api import get



### Funções de Apoio ###

# Função para checar se uma lista está vazia
def is_empty(list_var):
    if (len(list_var) == 0):
        return True
    else:
        return False

# Função para limpar as strings (usada na função "references()")
def clean_string(list_var):
    for i in range(len(list_var)):
        list_var[i] = list_var[i].replace("&#160;", "")
        list_var[i] = list_var[i].replace("&amp;", "")
        list_var[i] = list_var[i].replace('url= (ajuda)', "")
        list_var[i] = list_var[i].replace('&#124', "")
        list_var[i] = list_var[i].replace(";coautores= (ajuda)", "")
        list_var[i] = list_var[i].replace("['", "")
        list_var[i] = list_var[i].replace("']", "")
        list_var[i] = list_var[i].replace("[]", "Não tem")
        list_var[i] = list_var[i].replace("']", "")
        
# Função para remoção de duplicatas em listas
def remove_duplicates(list_var):
    # Criando uma lista vazia
    list_return = []
    
    # Tudo que não tiver na lista vazia, será inserido, e o que já tiver na lista, não será inserido
    for i in list_var:
        if i not in list_return:
            list_return.append(i)
    
    # Retorna a lista nova
    return list_return

# Função para pegar um link e transformar o html em texto
def transform_to_text():
    link = get_verify_link()
    page = requests.get(link)

    return page.text

# Função da primeira tela do programa
def start_screen():
    print("################################################")
    print("#        Bem-vindo(a) ao WikiScrapper!!        #")
    print("################################################\n")

    return transform_to_text()

# Função para imprimir a tela do menu
def menu_screen():
    print("\n################################################")
    print("#                     Menu                     #")
    print("#                                              #")
    print("#  1 - Listar tópicos do índice                #")
    print("#  2 - Listar nomes de arquivos de imagem      #")
    print("#  3 - Listar as referências bibliográficas    #")
    print("#  4 - Listar todos os links de outros artigos #")
    print("#  5 - Mudar de artigo                         #")
    print("#  6 - Sair do programa                        #")
    print("#                                              #")
    print("################################################\n")

# Função do menu
def menu(page_wiki):
    menu_screen()
    const_menu = "\nVoltando pro menu...\n"
    op = input("Digite sua opção: ")
    
    if op == '1':
        list_topics(page_wiki)
        print(const_menu)
        menu(page_wiki)
    elif op == '2':
        images_path(page_wiki)
        print(const_menu)
        menu(page_wiki)
    elif op == '3':
        references(page_wiki)
        print(const_menu)
        menu(page_wiki)
    elif op == '4':
        articles(page_wiki)
        print(const_menu)
        menu(page_wiki)
    elif op == '5':
        page_wiki = transform_to_text()
        print(const_menu)
        menu(page_wiki)
    elif op == '6':
        exit()
    else:
        print("Comando não reconhecido, tente novamente!")
        menu(page_wiki)



### Funções do Projeto ###

# Verificação do domínio do artigo
def get_verify_link():
    # Expressão regular para verificar o domínio da página
    regwiki = re.compile(r'https://pt.wikipedia.org/\w+/[%\w+]*\w+[%\w+]*')

    # Requisição ao usuário do link para ser avaliado
    link = input("Insira um link de uma página da pt.wikipédia: ")

    # Se o link se encaixar na ER, é imprimido no console que o domínio é válido, e a função retorna o link
    if regwiki.findall(link):
        print("\nO link tem domínio válido!\n")
        return link
    # Se o link não se encaixar na ER, imprime que o domínio é inválido e não retorna nada
    else:
        print("\nO link não tem o domínio exigido pelo programa!")
        print("\U0001F605")
        exit()

# Lista dos tópicos do índice do artigo
def list_topics(page):
    # Expressões regulares para identificar o número do tópico e o nome, respectivamente
    regnumtopic = re.compile(r'<span class="tocnumber">(\d+[.\d]*)</span>')
    regtopic = re.compile(r'<span class="toctext">(.*)</span>')

    # Encontrando strings que se encaixam nas ERs
    numtopics = regnumtopic.findall(page)
    topics = regtopic.findall(page)
    
    # Imprimindo o número e o nome dos tópicos equivalentes
    for i in range(len(numtopics)): 
        print("{} - {}".format(numtopics[i], topics[i]))

# Lista de todos os nomes de arquivos de imagem do artigo
def images_path(page):
    # Expressão regular para pegar os nomes dos arquivos de imagens que estão em conjunto
    regimages = re.compile(r'<div class="thumbimage"><a href="/wiki/Ficheiro:(\w+\W*\w+[%\w]*\W*\w+[%\w]*\W*\w+[%\w]*\W*\w+\W*\w+..\w+)" class="image"')
    # Expressão regular para pegar os nomes dos arquivos de iamgens individuais
    regsepimages = re.compile(r'<div class="thumbinner" style="width:\d+px;"><a href="/wiki/Ficheiro:(\w+\W*\w+[%\w]*\W*\w+[%\w]*\W*\w+[%\w]*\W*\w+.\w+)" class="image"')
    
    # Encontrando o nome dos arquivos e adicionando à lista images
    images = regimages.findall(page)

    # Adicionando à lista os arquivos encontrados pela outra ER
    for image in regsepimages.findall(page):
        images.append(image)

    # Organizando em ordem alfabética
    images.sort()
    
    print("Encontradas {} imagens".format(len(images)))

    # Imprimindo cada nome de arquivo das listas
    for image in images:
        print("- {}".format(image))

# Lista de todas as referências bibliográficas do artigo
def references(page):
    # Expressão regular para pegar todas as referências bibliográficas
    regref = re.compile(r'<span class="reference-text">(.*)</span>')

    # ER para retirar as marcações HTML
    regrefsub = re.compile(r'<.*?>|<i>')
    
    # Filtro para pegar os link
    regrefhref = re.compile(r'href="(.*?)">')


    # Lista geral de referências
    all_references = regref.findall(page)

    # Lista para pegar os links de cada referência
    links = []
    
    for i in range(len(all_references)):
        links.append(str(regrefhref.findall(all_references[i])))

    # Criando uma lista para passar os dados já substituídos
    references = []

    for i in range(len(all_references)):
        references.append(regrefsub.sub('', (all_references[i])))
    
    # Limpando as strings
    clean_string(references)
    clean_string(links)

    # Impressão do resultado
    for i in range(len(references)):
        print("{} - {}".format(i + 1, references[i]))
        print("Link - {}".format(links[i]))
        print("\n")

# Lista de todos os links para outros artigos da Wikipédia que são citados no artigo
def articles(page):
    # Expressão regular para pegar todos os links de artigos da Wikipedia citados no conteúdo do artigo passado pelo usuário
    reghref = re.compile(r'href="(/wiki/\w+[%\w+]*\w+[%\w+]*)"')

    # Lista para todos os artigos citados
    articles = reghref.findall(page)

    # Chamando uma função para retirar as duplicatas e atualizando a variável
    articles = remove_duplicates(articles)

    # Impressão do resultado com o link inteiro para o artigo
    for i in range(len(articles)):
        print("{} - https://pt.wikipedia.org{}".format(i + 1, articles[i]))



### Main ###

page_wiki = start_screen()
menu(page_wiki)
