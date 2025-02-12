import tkinter as tk
from menu_voo import create_flight_window
from menu_bus import create_bus_window

# Function to create the initial menu
def create_initial_menu():
    menu_root = tk.Tk()
    menu_root.title("Escolha o Tipo de Cotação")

    # Centering the window on the screen
    window_width, window_height = 300, 200
    screen_width, screen_height = menu_root.winfo_screenwidth(), menu_root.winfo_screenheight()
    position_top, position_right = (screen_height - window_height) // 2, (screen_width - window_width) // 2
    menu_root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    
    tk.Label(menu_root, text="Escolha o tipo de cotação:").pack(pady=20)
    tk.Button(menu_root, text="Cotação de Voo", command=create_flight_window).pack(pady=10)
    tk.Button(menu_root, text="Cotação de Ônibus", command=create_bus_window).pack(pady=10)

    menu_root.mainloop()

# Start the application with the initial menu
create_initial_menu()
