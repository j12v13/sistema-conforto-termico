import pandas as pd
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

@dataclass
class Rule:
    name: str
    condition: Callable[[Dict[str, float]], bool]
    label: str


def classify(row, rules: List[Rule]) -> Tuple[str, str]:
    """
    Motor de inferência:
    percorre as regras em ordem e retorna
    a primeira que for verdadeira
    """
    for r in rules:
        if r.condition(row):
            return r.label, r.name

    return "Confortável", "Regra padrão"


rules = [

    Rule(
        name="Regra Muito Frio",
        condition=lambda r: r['temperatura'] < 10,
        label="Muito Frio"
    ),

    Rule(
        name="Regra Muito Quente",
        condition=lambda r: r['temperatura'] > 35,
        label="Muito Quente"
    ),

    Rule(
        name="Regra Muito Seco",
        condition=lambda r: r['umidade'] < 30 and 10 <= r['temperatura'] <= 30,
        label="Muito Seco"
    ),

    Rule(
        name="Regra Muito Úmido",
        condition=lambda r: r['umidade'] > 80 and r['temperatura'] >= 20,
        label="Muito Úmido"
    ),

    Rule(
        name="Regra Precisa de Vento",
        condition=lambda r: r['temperatura'] > 28 and 40 <= r['umidade'] <= 70,
        label="Necessita Vento"
    ),

    Rule(
        name="Regra Precisa de Sol",
        condition=lambda r: r['temperatura'] < 20 and 40 <= r['umidade'] <= 70,
        label="Necessita Sol"
    )
]


data = pd.DataFrame({
    'temperatura': [5, 22, 40, 28, 18, 30, 24],
    'umidade': [50, 45, 60, 85, 20, 50, 55]
})


results = data.apply(lambda row: classify(row, rules), axis=1)

data['classificacao'] = [r[0] for r in results]
data['regra_ativada'] = [r[1] for r in results]


print(data)