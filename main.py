import json
import os

# Path to the JSON file in the executable directory
json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aeroportos.json')

# Load airports from JSON file
def load_airports():
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            return sorted(json.load(file), key=lambda x: x["Cidade"])
    return []

# Save airports to JSON file
def save_airports():
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(Aeroporto, file, ensure_ascii=False, indent=4)

# Airports List
Aeroporto = load_airports()

# Function to generate the quotation text
def gerar_cotacao(origem, destino, data_ida, hora_saida_ida, hora_chegada_ida, data_volta, hora_saida_volta, hora_chegada_volta, valor, somente_ida, paradas_ida, paradas_volta, bagagem_despachada):
    bagagem_texto = "Inclui: Bagagem de mão e bagagem despachada." if bagagem_despachada else "Inclui: Bagagem de mão (Sem bagagem despachada)."
    
    template = f"""Segue sua cotação especial para a sua próxima viagem! ✈

{origem} x {destino}

Ida: {{data_ida}}
➡ Saída: {{hora_saida_ida}} ({{paradas_ida}})
➡ Chegada: {{hora_chegada_ida}} em {destino}
"""
    if not somente_ida:
        template += f"""
Volta: {{data_volta}}
➡ Saída: {{hora_saida_volta}} ({{paradas_volta}})
➡ Chegada: {{hora_chegada_volta}} em {origem}
"""
    template += f"""
💰 Valor: R$ {{valor}} ({'somente ida' if somente_ida else 'ida e volta'})
{bagagem_texto}"""

    return template.format(
        data_ida=data_ida,
        hora_saida_ida=hora_saida_ida,
        hora_chegada_ida=hora_chegada_ida,
        data_volta=data_volta,
        hora_saida_volta=hora_saida_volta,
        hora_chegada_volta=hora_chegada_volta,
        valor=valor,
        paradas_ida=paradas_ida,
        paradas_volta=paradas_volta
    )
    
# Function to generate the bus quotation text
def gerar_cotacao_bus(origem, destino, data_ida, hora_saida_ida, hora_chegada_ida, data_volta, hora_saida_volta, hora_chegada_volta, valor, somente_ida):
    
    template = f"""Segue sua cotação especial para a sua próxima viagem! 🚌

{origem} x {destino}

Ida: {{data_ida}}
➡ Saída: {{hora_saida_ida}}
➡ Chegada: {{hora_chegada_ida}} em {destino}
"""
    if not somente_ida:
        template += f"""
Volta: {{data_volta}}
➡ Saída: {{hora_saida_volta}}
➡ Chegada: {{hora_chegada_volta}} em {origem}
"""
    template += f"""
💰 Valor: R$ {{valor}} ({'somente ida' if somente_ida else 'ida e volta'})
"""

    return template.format(
        data_ida=data_ida,
        hora_saida_ida=hora_saida_ida,
        hora_chegada_ida=hora_chegada_ida,
        data_volta=data_volta,
        hora_saida_volta=hora_saida_volta,
        hora_chegada_volta=hora_chegada_volta,
        valor=valor
    )
    