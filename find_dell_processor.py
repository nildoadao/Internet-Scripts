#!/usr/bin/env python3

import requests, sys, argparse, json
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Script em Python para obter o processor de servidores Dell.")

parser.add_argument("-tag",help="Service Tag", required=False)
parser.add_argument("-list",help="Lista de tags", required=False)

args=vars(parser.parse_args())

def find_processor(tag):

    # Link para suporte da Dell
    url = "https://www.dell.com/support/home/pt/br/04/product-support/servicetag/{}/configuration".format(tag)

    try:
        response = requests.get(url)
        results = []
        soap = BeautifulSoup(response.text, "html.parser")

        # dell/support carrega as informacoes na tag "hdnParts" no formato json
        hdn_parts = json.loads(soap.find(id="hdnParts").get("value"))

        for item in hdn_parts:
            for part in item[u"Parts"]:
                if "processor" in part[u"Description"].lower() and "memory" not in item[u"SkuDescription"].lower() and "heat" not in item[u"SkuDescription"].lower():
                    results.append(item[u"SkuDescription"])

        with open("processadores.csv", mode="a") as f:
            f.write("{};{}\n".format(tag, results[0]))  
        
        print("Service Tag: {}, Processador: {}".format(tag, results[0]))

    except (Exception) as e:

        if(type(e) is requests.exceptions.ConnectionError):
            raise e

        else:
            print("Service Tag: {}, falha ao obter processador.".format(tag))
            return  

if __name__ == "__main__":
    try:
        if (args["tag"]):
            tag = args["tag"]
            find_processor(tag)

        elif (args["list"]):
            tags = args["list"].split(",")
            for item in tags:
                find_processor(item)
        else:
            print("Erro, deve ser fornecido algum parametro para o script\nEx: find_dell_processor -tag ABCDGG")

    except (Exception) as e:

        if(type(e) is requests.exceptions.ConnectionError):
            print("Falha na comunicacao com dell.com/support, verifique a conexao e tente novamente")

        else:
            print("Service Tag invalida")

    sys.exit()

    