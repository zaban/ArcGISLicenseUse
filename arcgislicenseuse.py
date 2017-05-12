# -*- coding: utf-8 -*-
import sys, os
import subprocess

# SCRIPT CONFIGURATION
# Alter 'dir' variable to point 'lmutil.exe' path
# Alter 'clearScreen' variable according your OS (Windows = cls, Linux = clear)
dir = r"E:\Program Files (x86)\ArcGIS\License10.3\bin"
command = ["lmutil","lmstat","-a","-c","@lmgis.cesan.com.br"]
clearScreen = "cls"

# executa o comando lmutil e retorna o resultado
def RunLMUtil():
    # muda de diretório (evitando Permission Denied), executa o comando e recupera o resultado
    os.chdir(dir)
    output = subprocess.check_output(command)

    lineCounter = 1
    numChars = len(output)
    linha = ""
    linhas = []

    # percorre caracter por caracter da string de retorno, buscando por quebras de linha e
    # armazenando as linhas em um array
    for i in range(0, numChars - 2):
        
        #se encontra uma quebra de linha, armazena a mesma no array
        if (output[i:i+2] == '\r\n'):
            linhas.append(linha)
            linha = ""
            lineCounter += 1
        else:
            if (output[i:i+1] != '\n'):
                linha = linha + output[i:i+1]

    return linhas

def ProcessaLinhas(linhas):
    i = 0
    linhaInicioEditor = 0
    linhaInicioGrid = 0
    linhaInicioInterop = 0
    linhaFimEditor = 0
    linhaFimGrid = 0
    linhaFimInterop = 0
    UsuariosxLicencas = []

    # loop principal do array de linhas. Encontra as linhas de cada tipo de licença
    for linha in linhas:
        if (linha != ""):
            if (linha.find("Editor") > 0):
                linhaInicioEditor = i + 3
            if (linha.find("Grid") > 0):
                linhaInicioGrid = i + 3
                linhaFimEditor = i - 3
            if (linha.find("Interop") > 0):
                linhaInicioInterop = i + 3
                linhaFimGrid = i - 3       
        i += 1 
    linhaFimInterop = i - 1

    # preenche um array com o uso de licenças [tipo_lic][usuario]
    for i in range(linhaInicioEditor, linhaFimEditor):
        elemLinha = linhas[i].split(" ")
        #print(elemLinha[4])
        UsuariosxLicencas.append(["ArcGIS for Desktop",elemLinha[4],elemLinha[5]])

    for i in range(linhaInicioGrid, linhaFimGrid):
        elemLinha = linhas[i].split(" ")
        #print(elemLinha[4])
        UsuariosxLicencas.append(["Spatial Analist",elemLinha[4],elemLinha[5]])
    
    for i in range(linhaInicioInterop, linhaFimInterop):
        elemLinha = linhas[i].split(" ")
        #print(elemLinha[4])
        UsuariosxLicencas.append(["Data Interoperability",elemLinha[4],elemLinha[5]])
    
    return UsuariosxLicencas

# rotina principal
def main():
    subprocess.call([clearScreen], shell=True)
    print("Verificando uso de licencas. Aguarde...")
    print("-" * 79)

    #executa a checagem de uso de licenças e recebe o resultado
    output = RunLMUtil()

    #processa o resultado anterior e recebe array com o uso das licenças por tipo 
    resultado = ProcessaLinhas(output)
    resultado.sort()
    
    #imprime o resultado
    tipoLicenca = ""
    total = -1

    for registro in resultado:
        if (tipoLicenca != registro[0]):
            if (total >= 0):
                print("TOTAL: " + str(total))
                total = 0
            tipoLicenca = registro[0]
            print("\r\nLicencas " + tipoLicenca + ":")
            print("-" * 79)
        print(registro[1] + " - " + registro[2])
        total += 1
    print("TOTAL: " + str(total))
    
# redirecionador
if __name__ == "__main__":
    main()