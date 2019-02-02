#!/usr/bin/env python3

import requests, sys, argparse, json, warnings
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(description="Script em Python para obter o processor de servidores HPE.")

parser.add_argument("-serial",help="Serial number", required=False)
parser.add_argument("-list",help="Lista de seriais numbers", required=False)

args=vars(parser.parse_args())

def find_processor(tag):

    # Link para partsurfer HPE
    url = "https://partsurfer.hpe.com/Search.aspx?searchText={}".format(tag)

    try:
        response = requests.get(url, verify=False)
        soap = BeautifulSoup(response.text, "html.parser")
        previous_tag = soap.find_next("span")
        processor = "Nao encontrado."
        
        for item in soap.find_all("span"):
            if "logic cpu" in item.text.lower() and "proc" in previous_tag.text.lower():
                processor = previous_tag.text
            previous_tag = item
        
        # Em alguns casos o PartSufer da HP nao gera a coluna Logic CPU
        # Nesse caso e feita a busca direta pelo termo sps-proc
        if "Nao encontrado" in processor:
            for item in soap.find_all("span"):
                if "sps-proc" in item.text.lower():
                    processor = item.text

        with open("processadores.csv", mode="a") as f:
            f.write("{};{}\n".format(tag, processor))  

        print("Serial: {}, Processador: {}".format(tag, processor))

    except (Exception) as e:

        if(type(e) is requests.exceptions.ConnectionError):
            raise e

        else:
            print("Serial: {}, falha ao obter processador.".format(tag))
            return  

if __name__ == "__main__":
    try:
        if (args["serial"]):
            tag = args["serial"]
            find_processor(tag)

        elif (args["list"]):
            tags = args["list"].split(",")
            for item in tags:
                find_processor(item)
        else:
            print("Erro, deve ser fornecido algum parametro para o script\nEx: find_hpe_processor -serial ABCDGG")

    except (Exception) as e:

        if(type(e) is requests.exceptions.ConnectionError):
            print("Falha na comunicacao com patsurfer.hpe, verifique a conexao e tente novamente")

        else:
            print("Serial invalido")

    sys.exit()