import tkinter as tk
from tkinter import messagebox
import main

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

# Function to update the preview text
def update_preview():
    cotacao = main.gerar_cotacao_bus(
        var_origem.get(), var_destino.get(), entry_data_ida.get(), entry_hora_saida_ida.get(), entry_hora_chegada_ida.get(),
        entry_data_volta.get(), entry_hora_saida_volta.get(), entry_hora_chegada_volta.get(), entry_valor.get(), var_somente_ida.get()
    )
    text_preview.delete(1.0, tk.END)
    text_preview.insert(tk.END, cotacao)

# Function to generate and copy the quotation to clipboard
def gerar_e_copiar_cotacao():
    update_preview()
    root.clipboard_clear()
    root.clipboard_append(text_preview.get(1.0, tk.END))
    messagebox.showinfo("Cotação", "Cotação gerada e copiada para a área de transferência!")

# Function to create the main window for flight quotation
def create_bus_window():
    global root
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
    global entry_data_ida, entry_hora_saida_ida, entry_hora_chegada_ida, entry_data_volta, entry_hora_saida_volta, entry_hora_chegada_volta, entry_valor, var_origem, var_somente_ida, var_destino, text_preview
    entry_data_ida = create_labeled_entry(frame_ida, "Data Ida:", 0, 0, format_date)
    entry_hora_saida_ida = create_labeled_entry(frame_ida, "Saída:", 1, 0, format_time)
    entry_hora_chegada_ida = create_labeled_entry(frame_ida, "Chegada:", 2, 0, format_time)

    # Creating and placing the input fields for "Volta"
    entry_data_volta = create_labeled_entry(frame_volta, "Data Volta:", 0, 0, format_date)
    entry_hora_saida_volta = create_labeled_entry(frame_volta, "Saída:", 1, 0, format_time)
    entry_hora_chegada_volta = create_labeled_entry(frame_volta, "Chegada:", 2, 0, format_time)

    # Creating and placing the input field for "Valor"
    entry_valor = create_labeled_entry(root, "Valor:", 2, 0, lambda _: update_preview())

    # Creating and placing the checkbuttons
    var_somente_ida = tk.BooleanVar()
    check_somente_ida = tk.Checkbutton(root, text="Somente Ida", variable=var_somente_ida, command=update_preview)
    check_somente_ida.grid(row=3, column=0, columnspan=2, sticky="nsew")

    # Creating and placing the input fields for "Origem" and "Destino"
    tk.Label(root, text="Origem:").grid(row=0, column=0, sticky="e")
    var_origem = tk.StringVar()
    entry_origem = tk.Entry(root, textvariable=var_origem)
    entry_origem.grid(row=0, column=1, sticky="w")
    entry_origem.bind('<KeyRelease>', lambda _: update_preview())

    tk.Label(root, text="Destino:").grid(row=0, column=2, sticky="e")
    var_destino = tk.StringVar()
    entry_destino = tk.Entry(root, textvariable=var_destino)
    entry_destino.grid(row=0, column=3, sticky="w")
    entry_destino.bind('<KeyRelease>', lambda _: update_preview())

    # Creating and placing the buttons
    tk.Button(root, text="Gerar e Copiar Cotação", command=gerar_e_copiar_cotacao).grid(row=5, column=0, columnspan=2, sticky="nsew")
    
    # Creating and placing the text widget for preview
    text_preview = tk.Text(root, height=15, width=50)
    text_preview.grid(row=6, column=0, columnspan=4, sticky="nsew")
