

def ler_arquivo(arquivo):

    with open(arquivo) as f:

        # Ignora o cabeçalho do arquivo
        next(f)

        # Cria uma lista com os dados do arquivo
        dados = []
        
        for linha in f:
            
            # Separa os campos da linha pelo caractere ","
            campos = linha.strip().split(",")
            
            # Converte os dados do arquivo para os tipos corretos
            idade = int(campos[0])
            sexo = campos[1]
            tensao = int(campos[2])
            colesterol = int(campos[3])
            batimento = int(campos[4])
            tem_doenca = bool(int(campos[5]))
            
            # Adiciona os dados em um dicionário
            registo = {'idade': idade, 'sexo': sexo, 'tensao': tensao, 'colesterol': colesterol, 'batimento': batimento, 'temDoença': tem_doenca}
            dados.append(registo)
    
    # Retorna a lista com os dados do arquivo
    return dados



def distribuicao_doenca_por_sexo(modelo):
    
    # Conta o número total de registros de cada sexo
    contagem_por_sexo = {'M': 0, 'F': 0}
    
    # Conta o número de registros de cada sexo que têm a doença
    contagem_com_doenca_por_sexo = {'M': 0, 'F': 0}

    for registo in modelo:
        sexo = registo['sexo']
        tem_doenca = registo['temDoença']
        contagem_por_sexo[sexo] += 1
        if tem_doenca:
            contagem_com_doenca_por_sexo[sexo] += 1

    proporcao_doenca_por_sexo = {
        'M': contagem_com_doenca_por_sexo['M'],
        'Y': contagem_por_sexo['M'],
        'F': contagem_com_doenca_por_sexo['F'],
        'X': contagem_por_sexo['F']
    }

    return proporcao_doenca_por_sexo



def distribuicao_doenca_por_idade(modelo):
    
    # Define os limites dos escalões etários
    limites_idade = [(0, 4), (5, 9), (10, 14), (15, 19), (20, 24), (25, 29), (30, 34), (35, 39), (40, 44), (45, 49),
                     (50, 54), (55, 59), (60, 64), (65, 69), (70, 74), (75, 79), (80, 84), (85, 89), (90, 94), (95, 99)
                     , (100, 104), (105, 109), (110, 114)]

    # Inicializa os contadores
    contagem_por_idade = [0] * len(limites_idade)
    contagem_com_doenca_por_idade = [0] * len(limites_idade)

    # Agrupa os registros por escalão etário
    for registo in modelo:
        idade = registo['idade']
        tem_doenca = registo['temDoença']
        for i, (lim_inf, lim_sup) in enumerate(limites_idade):
            if lim_inf <= idade <= lim_sup:
                contagem_por_idade[i] += 1
                if tem_doenca:
                    contagem_com_doenca_por_idade[i] += 1
                break


    dados = []

    for i in range(len(limites_idade)):
        
        lim_inf, lim_sup = limites_idade[i]
        if contagem_por_idade[i] == 0:
            continue
        
        info = {'lim_inf': lim_inf, 'lim_sup': lim_sup, 'total': contagem_por_idade[i],
        'total_doentes': contagem_com_doenca_por_idade[i], 'percentagem': 100*(contagem_com_doenca_por_idade[i]/contagem_por_idade[i])}    

        dados.append(info)

        
    return dados



def distribuicao_doenca_por_colesterol(dados):
    
    # Obter o valor mínimo e máximo do colesterol
    colesterol_min = min(registro['colesterol'] for registro in dados)
    colesterol_max = max(registro['colesterol'] for registro in dados)


    # Calcular o número de intervalos
    num_intervalos = (colesterol_max - colesterol_min) // 10 + 1


    # Criar uma lista de intervalos de colesterol
    intervalos = [(colesterol_min + i * 10, colesterol_min + (i + 1) * 10 - 1) for i in range(num_intervalos)]


    # Contabilizar o número de registros em cada intervalo, ignorando casos com 0 de colesterol
    contagem = {intervalo: [0, 0] for intervalo in intervalos}


    for registro in dados:
        colesterol = registro['colesterol']
        intervalo = next(i for i, (limite_inf, limite_sup) in enumerate(intervalos) if limite_inf <= colesterol <= limite_sup)
        doente = registro['temDoença']
        
        if colesterol == 0:
            continue

        if doente:
            contagem[intervalos[intervalo]][0] += 1
            contagem[intervalos[intervalo]][1] += 1
        else:
            contagem[intervalos[intervalo]][1] += 1


    return contagem




def print_tabela(dados, choice):


    if choice == 1 or choice == 0:
        distribuicao_Sexo = distribuicao_doenca_por_sexo(dados)

        print("\n")
        print("Tabela da distribuição da doença por sexo:")

        print("-------------------------------------------------")
        print(f"|{'Sexo':^11} | {'Doentes':^8} | {'Total':^8} |  {'Proporção':^8} |")
        print("-------------------------------------------------")

        print(f"|  Masculino | {distribuicao_Sexo['M']:^8} | {distribuicao_Sexo['Y']:^8} |   {100*(distribuicao_Sexo['M']/distribuicao_Sexo['Y']):.2f}%   |")
        print(f"|  Feminino  | {distribuicao_Sexo['F']:^8} | {distribuicao_Sexo['X']:^8} |   {100*(distribuicao_Sexo['F']/distribuicao_Sexo['X']):.2f}%   |")

        print("-------------------------------------------------")




    if choice == 2 or choice == 0:
        distribuicao_Idade = distribuicao_doenca_por_idade(dados)

        print("\n")
        print("Tabela da distribuição da doença por escalões etários:")

        # Calcula o tamanho máximo de cada coluna
        max_intervalo = max(len(f"{i['lim_inf']}-{i['lim_sup']}") for i in distribuicao_Idade) + 1
        max_doentes = max(len(str(i['total_doentes'])) for i in distribuicao_Idade) + 4
        max_total = max(len(str(i['total'])) for i in distribuicao_Idade) + 4
        max_proporcao = max(len(f"{i['percentagem']:.2f}%") for i in distribuicao_Idade) 

        # Imprime a tabela com as colunas ajustadas
        print("-" * (max_intervalo + max_doentes + max_total + max_proporcao + 18))
        print(f"|{'Intervalo':<{max_intervalo}} | {'Doentes':^{max_doentes}} | {'Total':^{max_total}} | {'Proporção':^{max_proporcao}} |")
        print("-" * (max_intervalo + max_doentes + max_total + max_proporcao + 18))
        for i in distribuicao_Idade:
            print(f"|{i['lim_inf']}-{i['lim_sup']:<{max_intervalo}} | {i['total_doentes']:^{max_doentes}} | {i['total']:^{max_total}} | {i['percentagem']:.2f}%{' ':>{max_proporcao-3}} |")
            print("-" * (max_intervalo + max_doentes + max_total + max_proporcao + 18))





    if choice == 3 or choice == 0:
        distribuicao_colesterol = distribuicao_doenca_por_colesterol(dados)

        print("\n")
        print("Tabela da distribuição da doença por níveis de colesterol:")

        print("-----------------------------------------------------------------------")
        print(f"|{'Intervalo':^15} | {'Doentes':^15} | {'Total':^15} | {'Proporção':^15} |")
        print("-----------------------------------------------------------------------")

        proporcao_total = 0
        for limite, valor in distribuicao_colesterol.items():

            if valor[1] == 0:
                continue

            proporcao = 100*(valor[0]/valor[1])
            proporcao_total += proporcao

            print(f"|      {limite[0]}-{limite[1]}    | {valor[0]:^15} | {valor[1]:^15} |        {proporcao:.2f}% |")
            print("-----------------------------------------------------------------------")
    
    if choice < 0 or choice > 3:
        print("Erro na escolha da tabela!")







def main():

    arquivo = "myheart.csv"
    modelo = ler_arquivo(arquivo)
    

    print("0 - Imprimir todas as tabelas")
    print("1 - Tabela da distribuição da doença por sexo")
    print("2 - Tabela da distribuição da doença por idade")
    print("3 - Tabela da distribuição da doença por níveis de colesterol")

    opcao = int(input("Escolha uma opção (1, 2 ou 3): "))

    print_tabela(modelo, opcao)





if __name__ == '__main__':
    main()
