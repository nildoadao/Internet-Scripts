import hashlib, requests, argparse, sys

parser = argparse.ArgumentParser(description="Script to check leaked passwords")
parser.add_argument("-p",help="password to check", required=True)
args=vars(parser.parse_args())


def get_pwned_hashes(hash):
    # api from have i been pwned
    url = "https://api.pwnedpasswords.com/range/{}".format(hash)
    try:
        response = requests.get(url)
        if(response.status_code != 200):
            print("Erro ao buscar {} no banco de dados de pwned".format(hash))
            sys.exit()

        return response.text.splitlines()
    except:
        print("Falha ao obter uma resposta de api.pwnedpasswords.")
        sys.exit()


if __name__ == "__main__":

    full_hash = hashlib.sha1(args["p"]).hexdigest()
    hash_list = get_pwned_hashes(full_hash[:5])

    for hash in hash_list:     
        pass_hash, apearences = hash.split(":")

        if(pass_hash.lower() == full_hash[5:].lower()):
            print("{} foi encontrada !".format(args["p"]))
            print("Hash {} encontrado {} vezes".format(pass_hash, apearences))
            sys.exit()
    
    print("Senha nao encontrada")
        

