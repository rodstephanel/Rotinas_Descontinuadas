import os
import pandas as pd 
from PySimpleGUI import PySimpleGUI as sg

def layout():
    #Layout
    sg.theme('Reddit')
    layout = [
        [sg.Text('Arquivo CSV'), sg.Input(key='arquivoCSV')], #Arquivo CSV contendo a lista de rotinas descontinuadas
        [sg.Text('Local dos arquivos'),sg.Input(key='localArquivo')], #Local onde se encontra os programas fontes do Protheus
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
            process(valores["arquivoCSV"], valores["localArquivo"])
            break

def process(caminhoArq, diretorio):

    # Importa lista de rotinas contidas no CSV
    rotinasDescontinuadas = pd.read_csv(caminhoArq, sep =';', usecols=['Codigo-Fonte'])
    rotinasDescontinuadas.head()

    # Substitui os .prw por () e transforma em uma lista set
    setRotinasDescontinuadas = set([w.replace('.prw', "()") for w in rotinasDescontinuadas['Codigo-Fonte'].to_list()])
    print(f"setRotinasDescontinuadas= {setRotinasDescontinuadas}")
    
    #Abre/cria arquivo para colocar os resultados
    relResultado = open("Relatorio de resultados.csv", "w")
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
                compara = ','.join(list(compara))
                print(f"Foi verificado funcoes {compara} descontinuadas no arquivo {arquivo}")
                relResultado.write(f"{compara};{arqVerificado.name}\n")

    relResultado.close()
    

if __name__ == "__main__":

    layout()
    print("FIM")