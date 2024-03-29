import os

from pulp import *


def extract_data_from_csv(path):
    data = {}

    with open(path, 'r') as file:
        header = file.readline()
        keys = [k.strip() for k in header.split(',')]

        for line in file.readlines():
            values = line.strip().split(',')

            data_key = values.pop(0)

            data[data_key] = { x: y for x,y in zip(keys[1:], values) }

    return data


current_dir = os.path.dirname(os.path.abspath(__file__))

atividades = extract_data_from_csv(os.path.join(current_dir, 'inputs/atividades.csv'))
terreno = extract_data_from_csv(os.path.join(current_dir, 'inputs/terreno.csv'))
producao = extract_data_from_csv(os.path.join(current_dir, 'inputs/producao.csv'))

problem = LpProblem('ProjetoSertao', LpMaximize)


tipo_atividade = list(atividades.keys())
tipo_terreno = list(terreno.keys())


qtd_prod_terreno = { f'{t}_{a}': int(producao[a][t]) for a in tipo_atividade for t in tipo_terreno }

valor_venda_atividade = { a: float(atividades[a]['valor_venda']) for a in tipo_atividade }
custo_prep_terreno = { t: float(terreno[t]['custo_prep']) for t in tipo_terreno }
qtd_lucro_terreno = { f'{t}_{a}': valor_venda_atividade[a] - custo_prep_terreno[t] for a in tipo_atividade for t in tipo_terreno }


tipo_producao = [f'{t}_{a}' for a in tipo_atividade for t in tipo_terreno]

atividades_vars = LpVariable.dicts('atividades', tipo_producao, lowBound=0)

problem += lpSum([atividades_vars[tp] * qtd_lucro_terreno[tp] * qtd_prod_terreno[tp] for tp in tipo_producao]), 'Funcao objetivo'



qtd_hectare_terreno = { t: int(terreno[t]['hectare']) for t in tipo_terreno }
qtd_contrato_atividade = { a: int(atividades[a]['qtd_contrato']) for a in tipo_atividade }


for t in tipo_terreno:
    problem += lpSum([atividades_vars[tp] for tp in tipo_producao if t in tp]) <= qtd_hectare_terreno[t]

for a in tipo_atividade:
    problem += lpSum([qtd_prod_terreno[tp] * atividades_vars[tp] for tp in tipo_producao if a in tp]) >= qtd_contrato_atividade[a]

print('\n')
print(problem)

problem.solve()


solution = {
    1: 'Ótima',
    0: "Não resolvido",
    -1: 'Inviável',
    -2: 'Não vinculado',
    -3: 'Indefinido'
}


print('\nSolução:')
print(solution[problem.status])

print('\nDistribuição (Produção/ha):')
for v in problem.variables():
    print(f'{v.name}:', f'{v.varValue}ha')

print('\nLucro total:')
print('R$ {:.2f}'.format(value(problem.objective)))
