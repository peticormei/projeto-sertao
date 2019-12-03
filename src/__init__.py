from pulp import *


def extract_data_from_csv(path):
    iterable = []

    with open(path, 'r') as file:
        header = file.readline()
        keys = [k.strip() for k in header.split(',')]

        for line in file.readlines():
            values = line.strip().split(',')
            iterable.append({x: y for x,y in zip(keys, values)})

    return iterable, header


atividades, header_atv = extract_data_from_csv('src/atividades.csv')
terreno, header_ter = extract_data_from_csv('src/terreno.csv')

prob = LpProblem('ProjetoSertao', LpMaximize)

x1 = LpVariable("x1", lowBound=0)
x2 = LpVariable("x2", lowBound=0)

prob += 20*x1 + 30*x2
prob += 1*x1 + 2*x2 <= 100
prob += 2*x1 + 1*x2 <= 100

prob.solve()

print("Status:", LpStatus[prob.status])

for v in prob.variables():
    print(v.name, "=", v.varValue)

print("Total = ", value(prob.objective))
