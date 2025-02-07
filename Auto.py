import tkinter as tk
from tkinter import messagebox
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

# Function to format the date input
def format_date(event):
    text = event.widget.get()
    if len(text) in {2, 5}:
        event.widget.insert(tk.END, '/')
    update_preview()

# Function to format the time input
def format_time(event):
    text = event.widget.get()
    if len(text) == 2:
        event.widget.insert(tk.END, ':')
    update_preview()

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

# Function to update the preview text
def update_preview():
    cotacao = gerar_cotacao(
        var_origem.get(), var_destino.get(), entry_data_ida.get(), entry_hora_saida_ida.get(), entry_hora_chegada_ida.get(),
        entry_data_volta.get(), entry_hora_saida_volta.get(), entry_hora_chegada_volta.get(), entry_valor.get(),
        var_somente_ida.get(), var_paradas_ida.get(), var_paradas_volta.get(), var_bagagem_despachada.get()
    )
    text_preview.delete(1.0, tk.END)
    text_preview.insert(tk.END, cotacao)

# Function to generate and copy the quotation to clipboard
def gerar_e_copiar_cotacao():
    update_preview()
    root.clipboard_clear()
    root.clipboard_append(text_preview.get(1.0, tk.END))
    messagebox.showinfo("Cotação", "Cotação gerada e copiada para a área de transferência!")

# Function to add a new airport
def adicionar_aeroporto():
    def salvar_aeroporto():
        cidade = entry_cidade.get()
        iata = entry_iata.get()
        if cidade and iata:
            Aeroporto.append({"Cidade": cidade, "IATA": iata})
            Aeroporto.sort(key=lambda x: x["Cidade"])
            save_airports()
            atualizar_dropdowns()
            janela_adicionar.destroy()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    janela_adicionar = tk.Toplevel(root)
    janela_adicionar.title("Adicionar Aeroporto")

    tk.Label(janela_adicionar, text="Cidade:").grid(row=0, column=0)
    entry_cidade = tk.Entry(janela_adicionar)
    entry_cidade.grid(row=0, column=1)

    tk.Label(janela_adicionar, text="IATA:").grid(row=1, column=0)
    entry_iata = tk.Entry(janela_adicionar)
    entry_iata.grid(row=1, column=1)

    tk.Button(janela_adicionar, text="Salvar", command=salvar_aeroporto).grid(row=2, columnspan=2)

# Function to update the dropdown menus
def atualizar_dropdowns():
    for menu, var in [(option_origem["menu"], var_origem), (option_destino["menu"], var_destino)]:
        menu.delete(0, "end")
        for aeroporto in Aeroporto:
            label = f'{aeroporto["Cidade"]} ({aeroporto["IATA"]})'
            menu.add_command(label=label, command=lambda value=label: var.set(value))

# Creating the main window
root = tk.Tk()
root.title("Gerador de Cotação")

# Centering the window on the screen
window_width, window_height = 525, 600
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
position_top, position_right = (screen_height - window_height) // 2, (screen_width - window_width) // 2
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Configuring grid to expand and fill space
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(6, weight=1)

# Creating frames for better organization
frame_ida = tk.LabelFrame(root, text="Ida")
frame_ida.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

frame_volta = tk.LabelFrame(root, text="Volta")
frame_volta.grid(row=1, column=2, padx=10, pady=10, sticky="nsew", columnspan=2)

# Helper function to create labeled entries
def create_labeled_entry(frame, label_text, row, column, bind_func=None):
    tk.Label(frame, text=label_text).grid(row=row, column=column, sticky="e")
    entry = tk.Entry(frame)
    entry.grid(row=row, column=column + 1, sticky="w")
    if bind_func:
        entry.bind('<KeyRelease>', bind_func)
    return entry

# Creating and placing the input fields for "Ida"
entry_data_ida = create_labeled_entry(frame_ida, "Data Ida:", 0, 0, format_date)
entry_hora_saida_ida = create_labeled_entry(frame_ida, "Saída:", 1, 0, format_time)
entry_hora_chegada_ida = create_labeled_entry(frame_ida, "Chegada:", 2, 0, format_time)

tk.Label(frame_ida, text="Paradas Ida:").grid(row=3, column=0, sticky="e")
var_paradas_ida = tk.StringVar(root, "01 parada")
option_paradas_ida = tk.OptionMenu(frame_ida, var_paradas_ida, "Vôo direto", "01 parada", "02 paradas", "03 paradas", command=lambda _: update_preview())
option_paradas_ida.grid(row=3, column=1, sticky="w")

# Creating and placing the input fields for "Volta"
entry_data_volta = create_labeled_entry(frame_volta, "Data Volta:", 0, 0, format_date)
entry_hora_saida_volta = create_labeled_entry(frame_volta, "Saída:", 1, 0, format_time)
entry_hora_chegada_volta = create_labeled_entry(frame_volta, "Chegada:", 2, 0, format_time)

tk.Label(frame_volta, text="Paradas Volta:").grid(row=3, column=0, sticky="e")
var_paradas_volta = tk.StringVar(root, "01 parada")
option_paradas_volta = tk.OptionMenu(frame_volta, var_paradas_volta, "Vôo direto", "01 parada", "02 paradas", "03 paradas", command=lambda _: update_preview())
option_paradas_volta.grid(row=3, column=1, sticky="w")

# Creating and placing the input field for "Valor"
entry_valor = create_labeled_entry(root, "Valor:", 2, 0, lambda event: update_preview())

# Creating and placing the checkbuttons
var_somente_ida = tk.BooleanVar()
check_somente_ida = tk.Checkbutton(root, text="Somente Ida", variable=var_somente_ida, command=update_preview)
check_somente_ida.grid(row=3, column=0, columnspan=2, sticky="nsew")

var_bagagem_despachada = tk.BooleanVar()
check_bagagem_despachada = tk.Checkbutton(root, text="Bagagem Despachada", variable=var_bagagem_despachada, command=update_preview)
check_bagagem_despachada.grid(row=4, column=0, columnspan=2, sticky="nsew")

# Creating and placing the dropdowns for "Origem" and "Destino"
tk.Label(root, text="Origem:").grid(row=0, column=0, sticky="e")
var_origem = tk.StringVar(root, f'{Aeroporto[0]["Cidade"]} ({Aeroporto[0]["IATA"]})')
option_origem = tk.OptionMenu(root, var_origem, *[f'{a["Cidade"]} ({a["IATA"]})' for a in Aeroporto], command=lambda _: update_preview())
option_origem.grid(row=0, column=1, sticky="w")

tk.Label(root, text="Destino:").grid(row=0, column=2, sticky="e")
var_destino = tk.StringVar(root, f'{Aeroporto[1]["Cidade"]} ({Aeroporto[1]["IATA"]})')
option_destino = tk.OptionMenu(root, var_destino, *[f'{a["Cidade"]} ({a["IATA"]})' for a in Aeroporto], command=lambda _: update_preview())
option_destino.grid(row=0, column=3, sticky="w")

# Creating and placing the buttons
tk.Button(root, text="Adicionar Aeroporto", command=adicionar_aeroporto).grid(row=5, column=0, columnspan=2, sticky="nsew")
tk.Button(root, text="Gerar e Copiar Cotação", command=gerar_e_copiar_cotacao).grid(row=5, column=2, columnspan=2, sticky="nsew")

# Creating and placing the text widget for preview
text_preview = tk.Text(root, height=15, width=50)
text_preview.grid(row=6, column=0, columnspan=4, sticky="nsew")

# Running the main loop
root.mainloop()
