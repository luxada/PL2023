import re
import json

alunos = []
comp = re.compile(r'(\w+)({(\d+)}|{(\d+),(\d+)})?(::(\w+))?')

with open("input.csv") as f:
    cabecalho = f.readline()
    regex = r''
    campos = comp.findall(cabecalho)
    camposListas = []
    camposAgreg = []

    print(campos)
    for campo in campos:
        if campo[1] == '': # Não é uma lista
            regex += rf'(?P<{campo[0]}>[\w\s]+),'
        else: # É uma lista
            if campo[2] != '': # É uma lista fixa
                regex += rf'(?P<{campo[0]}>'
                regex += rf'([\w\s]+,*)' + '{' + campo[2] + '}),'
            else: # É uma lista com intervalo de tamanhos
                regex += rf'(?P<{campo[0]}>'
                regex += rf'(([\w\s]+)?,*)' + '{' + campo[4] + '}),'
            
            if campo[6] != '': # Temos uma função de agregação
                camposAgreg.append((campo[0],campo[6]))

            camposListas.append(campo[0])

    regex = regex[:-1]
    print(regex)
    comp = re.compile(regex)
    for line in f.readlines():
        line = line.replace("\n", "")
        ent = comp.search(line)

        if ent:
            dic = ent.groupdict()

            for campoLista in camposListas:
                lista = dic[campoLista].split(",")
                dic[campoLista] = []

                for elem in lista:
                    if elem != '':
                        dic[campoLista].append(elem)

                for (x, y) in camposAgreg:
                    if x == campoLista:
                        if y == "sum":
                            soma = 0
                            for elem in dic[campoLista]:
                                soma += int(elem)

                            dic[campoLista] = soma
                        elif y == "media":
                            soma = 0
                            for elem in dic[campoLista]:
                                soma += int(elem)

                            dic[campoLista] = soma / len(dic[campoLista])

            print(dic[campoLista])
            alunos.append(dic)
        else:
            print("Fudeu")


print(alunos)
jsonStr = json.dumps(alunos, indent = 2, ensure_ascii = False)
fout = open("output.json", "w")
fout.write(jsonStr)
fout.close()