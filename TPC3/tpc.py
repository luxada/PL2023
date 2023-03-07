import re
import json
from collections import Counter


def frequente_ano():
    # Abre o arquivo para leitura
    arquivo = open('processos.txt', 'r')

    # Cria um dicionário para contar a frequência de processos por ano
    freq_por_ano = {}

    # Itera sobre cada linha do arquivo
    for linha in arquivo:
        # Utiliza expressão regular para extrair o ano do processo
        ano = re.search(r'^\w+::(\d{4})', linha)
        if ano:
            # Incrementa o contador de processos para o ano correspondente
            if ano.group(1) in freq_por_ano:
                freq_por_ano[ano.group(1)] += 1
            else:
                freq_por_ano[ano.group(1)] = 1

    # Fecha o arquivo
    arquivo.close()


    return freq_por_ano

    
def frequencia_nomes_por_seculo(arquivo):
    # Expressão regular para extrair a data de cada processo
    data_regex = re.compile(r'\d{4}-\d{2}-\d{2}')

    # Dicionário para contar a frequência de nomes por século
    nomes_por_seculo = {}

    with open(arquivo, 'r', encoding='utf-8') as f:
        for line in f:
            # Extrai a data de cada linha
            data_str = data_regex.search(line)
            if data_str:
                data = int(data_str.group()[:4])

                # Determina o século a que o ano pertence
                seculo = (data - 1) // 100 + 1

                # Extrai o primeiro nome e o último sobrenome de cada nome completo
                campos = line.split('::')
                if len(campos) >= 4:
                    nome_completo = campos[2]
                    campos = line.strip().split("::")
                    nome_completo = campos[2]
                    if " " in nome_completo:
                        primeiro_nome, *_, ultimo_sobrenome = nome_completo.split()
                    else:
                        continue

                    # Conta a frequência de cada nome próprio e apelido por século
                    nomes_por_seculo.setdefault(seculo, {'nomes': Counter(), 'apelidos': Counter()})
                    nomes_por_seculo[seculo]['apelidos'][ultimo_sobrenome] += 1
                    nomes_por_seculo[seculo]['nomes'][primeiro_nome] += 1

    # Retorna os 5 nomes próprios e apelidos mais frequentes por século
    freq_nomes_por_seculo = {}
    for seculo, freq in sorted(nomes_por_seculo.items()):
        freq_nomes_por_seculo[seculo] = {
            'nomes': dict(freq['nomes'].most_common(5)),
            'apelidos': dict(freq['apelidos'].most_common(5))
        }

    return freq_nomes_por_seculo


def to_json():
    # Abre o arquivo de entrada e o arquivo de saída
    entrada = open('processos.txt', 'r')
    saida = open('primeiros_processos.json', 'w')

    # Cria uma lista vazia para armazenar os registros
    registros = []

    # Lê as primeiras 20 linhas do arquivo de entrada
    for i in range(20):
        linha = entrada.readline().strip()

        # Utiliza expressão regular para extrair os dados do registro
        dados = re.split(r'::', linha)

        # Cria um dicionário com os dados do registro
        registro = {
            'Pasta': dados[0],
            'Data': dados[1],
            'Nome': dados[2],
            'Pai': dados[3],
            'Mae': dados[4],
            'Observacoes': dados[5]
        }

        # Adiciona o registro à lista de registros
        registros.append(registro)

    # Escreve a lista de registros no arquivo de saída no formato JSON
    json.dump(registros, saida, indent = 2)

    # Fecha os arquivos de entrada e saída
    entrada.close()
    saida.close()




def tipo_relacao():
    dic = {}
    file = open("processos.txt")
    exp = re.compile(r",(?P<Relacao>(?:Pai|Filho|Irmao|Avo|Neto|Tio|Sobrinho|Mae|Primo|Tia|Prima|Sobrinha|Irma|Filha)\b[^.]*).")
    dic = {}

    for line in file.readlines():
        info = exp.findall(line)
        if info != []:
            for r in info:
                if r not in dic.keys():
                    dic[r] = 1
                else:
                    dic[r] +=1 
    return dic




def main():

    #Alinea A
    alinea_A = frequente_ano()

    # Ordena as chaves do dicionário em ordem crescente
    anos_ordenados = sorted(alinea_A.keys())

    # Imprime a frequência de processos por ano
    for ano in anos_ordenados:
        print(f"{ano}: {alinea_A[ano]}")
    

    #Alinea B
    alineaB = frequencia_nomes_por_seculo("processos.txt")

    print(alineaB)

    #Alinea C
    to_json()

    #AlineaD
    alineaD = tipo_relacao()

    for relacao, valor in alineaD.items():
        print(f"{relacao}: {valor}")






if __name__ == '__main__':
    main()