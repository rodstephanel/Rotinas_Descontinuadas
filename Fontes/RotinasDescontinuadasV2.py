import os
import pandas as pd 
from PySimpleGUI import PySimpleGUI as sg


def layout():
    #Layout
    sg.theme('DarkGrey5')
    layout = [
        [sg.Text('Lista CSV: ') ,sg.Input(), sg.FileBrowse(key='arquivo_CSV')],
        [sg.Text('Local dos arquivos do projeto: '),sg.Input(), sg.FolderBrowse(key='local_arquivo')],
        [sg.Text('Local para salvar o relatorio gerado: '),sg.Input(), sg.FolderBrowse(key='local_nv_arq')],
        [sg.Text('Nome do relatorio: '),sg.Input(key='nome_rel')],
        [sg.Button('Processar')]
    ]
    
    #Janela
    janela = sg.Window('Informações',layout)
    
    #Ler os eventos
    while True:
        eventos, valores = janela.read()
        if eventos == sg.WINDOW_CLOSED:
            break
        if eventos == 'Processar':
            process(valores["arquivo_CSV"], valores["local_arquivo"], valores["local_nv_arq"], valores["nome_rel"])
            break

def process(caminhoArq, diretorio, caminho_rel, nome_rel):

    # Importa lista de rotinas contidas no CSV
    rotinasDescontinuadas = pd.read_csv(caminhoArq, sep =';', usecols=['Codigo-Fonte'])
    rotinasDescontinuadas.head()

    # Substitui os .prw por () e transforma em uma lista set
    setRotinasDescontinuadas = set([w.replace('.prw', "()") for w in rotinasDescontinuadas['Codigo-Fonte'].to_list()])
    print(f"setRotinasDescontinuadas= {setRotinasDescontinuadas}")
    
    #Abre/cria arquivo para colocar os resultados
    #caminho_relatorio = os.path.realpath("C:\\Users\\RODRIGO ST\\Desktop\\BSO")
    caminho_relatorio = os.path.realpath(caminho_rel)
    relResultado = open(os.path.join(caminho_relatorio, nome_rel + ".csv"), "w")
    relResultado.write("Funcao;Local\n")

    #Percorre todo o diretório indicado
    for arqDiretorio, arqSubpasta, arquivos in os.walk(diretorio):

        print(f"arqDiretorio={arqDiretorio} arqSubpasta={arqSubpasta} arquivo={arquivos}")
        caminhoDir = os.path.realpath(arqDiretorio)

        for arquivo in arquivos:

            #Abre o arquivo e le ele todo
            arqVerificado = open(os.path.join(caminhoDir,arquivo), "r", encoding='utf-8',  errors='ignore')
            textArqVerficado = arqVerificado.read()
            arqVerificado.close()

            #Remove \n e faz o split do texto para fazer a comparacao com a lista de rotinas
            textArqVerficado = textArqVerficado.strip('\n').split()
            compara = setRotinasDescontinuadas & set(textArqVerficado)

            if len(compara) != 0:
                compara = ','.join(list(compara)).replace("()","")
                print(f"Foi verificado funcoes {compara} descontinuadas no arquivo {arquivo}")
                relResultado.write(f"{compara};{arqVerificado.name}\n")
            #else:
            #   print(f"Nao foi encontrado nenhuma palavra nesse arquivo {arquivo}")
    relResultado.close()
    

if __name__ == "__main__":

    layout()
    print("FIM ;)")