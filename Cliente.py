import socket, os, sys
from time import sleep
from pathlib import Path
from datetime import date, time, datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

current_date = date.today()
current_datetime = datetime.now()

# cria um objeto socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_servidor = "127.0.0.1"  # substitua pelo endereço IP do servidor
porta_servidor = 8888 # substitua pelo número da porta do servidor

# username will be set in login

def login():
    global username, BOOKING_FILE, AUDIT_FILE
    login_window = tk.Tk()
    login_window.title("Login - Cliente Agendamento")
    login_window.geometry("300x150")

    tk.Label(login_window, text="Digite o ID:").pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    def connect():
        global username, BOOKING_FILE, AUDIT_FILE
        username = username_entry.get()

        if username == '':
            messagebox.showerror("Erro", "Por favor, insira um User ID.")
            return
        elif username.isdigit():
            messagebox.showerror("Erro", "Insira um ID que contenha caracteres...")
            return
        else:
            try:
                cliente.connect((ip_servidor, porta_servidor))
                cliente.send(username.encode("utf-8")[:1020])
                BOOKING_FILE = Path(f"booking{current_date}_{username}.txt")
                AUDIT_FILE = Path(f"audit_{username}.txt")
                login_window.destroy()
                interface()
            except ConnectionRefusedError:
                messagebox.showerror("Erro", "Nenhuma conexão foi feita porque a máquina alvo rejeitou/não activa.")

    tk.Button(login_window, text="Conectar", command=connect).pack(pady=10)
    login_window.mainloop()

SCHEDULES_FILE = Path("schedules.txt")

def interface():
    root = tk.Tk()
    root.title("Cliente - Agendamento Distribuído")
    root.geometry("600x400")

    # Text area for outputs
    text_area = scrolledtext.ScrolledText(root, height=15, width=70)
    text_area.pack(pady=10)

    # Buttons
    btn_list_slots = tk.Button(root, text="Listar Slots Disponíveis", command=lambda: listar_slots_gui(text_area))
    btn_list_slots.pack(pady=5)

    btn_reserve = tk.Button(root, text="Reservar um Slot", command=lambda: reservar_slot_gui(username, text_area))
    btn_reserve.pack(pady=5)

    btn_my_reservations = tk.Button(root, text="Listar Minhas Reservas", command=lambda: reservas_user_gui(username, text_area))
    btn_my_reservations.pack(pady=5)

    btn_cancel = tk.Button(root, text="Cancelar uma Reserva", command=lambda: cancelar_reserva_gui(username, text_area))
    btn_cancel.pack(pady=5)

    btn_logs = tk.Button(root, text="Visualizar Logs", command=lambda: view_logs_gui(text_area))
    btn_logs.pack(pady=5)

    btn_delete = tk.Button(root, text="Apagar Dados", command=lambda: delete_data_gui(text_area))
    btn_delete.pack(pady=5)

    btn_clear = tk.Button(root, text="Limpar Tela", command=lambda: text_area.delete(1.0, tk.END))
    btn_clear.pack(pady=5)

    btn_exit = tk.Button(root, text="Exit", command=root.quit)
    btn_exit.pack(pady=5)

    root.mainloop()

def listar_slots_gui(text_area):
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, "=" * 8 + " SLOTS DISPONIVEIS " + "=" * 8 + "\n")
    text_area.insert(tk.END, f"Data:{current_date} - Slots disponíveis:\n")
    
    if SCHEDULES_FILE.exists():
        with open(SCHEDULES_FILE, 'r') as f:
            f_char = f.read(1)  

        if not f_char:
            with open(SCHEDULES_FILE, "a") as f:
                for x in range(8, 21):
                    f.write(f">> {time(x)}\n")

        with open(SCHEDULES_FILE) as f:
            content = f.read()
            text_area.insert(tk.END, content)
    else:
        file = open(SCHEDULES_FILE, "x")
        with open(SCHEDULES_FILE, "a") as f:
            for x in range(8, 21):
                f.write(f">> {time(x)}\n")

        with open(SCHEDULES_FILE) as f:
            content = f.read()
            text_area.insert(tk.END, content)
            f.close()

    if AUDIT_FILE.exists():
        with open(AUDIT_FILE, "a") as f:
            f.write(f"{current_datetime} | LIST_SLOTS | SYSTEM | {current_date}\n")
    else:
        file = open(AUDIT_FILE, "x")
        with open(AUDIT_FILE, "a") as f:
            f.write(f"{current_datetime} | LIST_SLOTS | SYSTEM | {current_date}\n")

def reservar_slot_gui(username, text_area):
    header = "=" * 8 + " RESERVAR SLOTS " + "=" * 8 + "\n"
    if text_area.get(1.0, tk.END).strip() == "":
        text_area.insert(tk.END, header)
    else:
        text_area.insert(tk.END, "\n" + header)
    try:
        comand = simpledialog.askinteger("Reservar Slot", "Insira o slot/hora para fazer a reserva [8-20]:")
        if comand is None:
            return
        
        if comand < 8 or comand >= 21:
            messagebox.showerror("Erro", "Slot indisponível neste horário!")
            return

        slot_time = time(comand)
        slot_key = f"slot::{current_date}:{slot_time}"

        slot_time_str = slot_time.strftime("%X")
        
        with open(rf"{SCHEDULES_FILE}", "r") as f:
            content = f.read()
            if slot_time_str in content:
                if BOOKING_FILE.exists() and AUDIT_FILE.exists():
                    with open(BOOKING_FILE, "a") as f:
                        f.write(f"{slot_key}\n")
                    
                    with open(AUDIT_FILE, "a") as f:
                        f.write(f"{current_datetime} | BOOK_SUCCESS | {username} | {slot_key}\n")
                else:
                    file = open(BOOKING_FILE, "x")
                    with open(BOOKING_FILE, "a") as f:
                        f.write(f"{slot_key}")

                    file = open(AUDIT_FILE, "x")
                    with open(AUDIT_FILE, "a") as f:
                        f.write(f"{current_datetime} | BOOK_SUCCESS | {username} | {slot_key}\n")
            
                with open(SCHEDULES_FILE, "r+") as f: 
                    lines = [line for line in f if line.strip() != f">> {slot_time_str}"]
                    f.seek(0)
                    f.writelines(lines)
                    f.truncate()
                
                text_area.insert(tk.END, "Reserva realizada com sucesso!\n")
                text_area.insert(tk.END, f"{current_date} às {slot_time_str}\n")
            
            else:
                text_area.insert(tk.END, "Falha na reserva - slot já ocupado ou indisponível!\n")
                with open(AUDIT_FILE, "a") as f:
                        f.write(f"{current_datetime} | BOOK_FAILED | {slot_key} - ocupado ou indisponível\n")

    except ValueError:
        messagebox.showerror("Erro", "Inserção do slot não é válida!!")

def reservas_user_gui(username, text_area):
    header = "=" * 8 + " MINHAS RESERVAS " + "=" * 8 + "\n"
    if text_area.get(1.0, tk.END).strip() == "":
        text_area.insert(tk.END, header)
    else:
        text_area.insert(tk.END, "\n" + header)
    try:
        if BOOKING_FILE.exists():
            with open(BOOKING_FILE) as f:
                content = f.read()
                text_area.insert(tk.END, content)
            
            with open(BOOKING_FILE, 'r') as f:
                f_char = f.read(1)
            
            if not f_char:
                text_area.insert(tk.END, "Nenhuma reserva foi feita...")
        else:
            file = open(BOOKING_FILE, "x")
            with open(BOOKING_FILE) as f:
                content = f.read()
                text_area.insert(tk.END, content)
                
            with open(BOOKING_FILE, 'r') as f:
                f_char = f.read(0)
            
            if not f_char:
                text_area.insert(tk.END, "Nenhuma reserva foi feita...")

        with open(BOOKING_FILE, 'r') as f:
            count = sum(1 for line in f)

        if AUDIT_FILE.exists():
            with open(AUDIT_FILE, "a") as f:
                f.write(f"{current_datetime} | LIST_USER_BOOKINGS | {username} | count: {count}\n")

    except FileNotFoundError:
        text_area.insert(tk.END, "ERRO: audit.tx ou booking.txt não existem...")

def cancelar_reserva_gui(username, text_area):
    header = "=" * 8 + " CANCELAR RESERVA " + "=" * 8 + "\n"
    if text_area.get(1.0, tk.END).strip() == "":
        text_area.insert(tk.END, header)
    else:
        text_area.insert(tk.END, "\n" + header)
    # Verifica ficheiro de reservas está vazio
    if BOOKING_FILE.exists():
        with open(BOOKING_FILE, 'r') as f:
            f_char = f.read(1)
            
        if not f_char:
            text_area.insert(tk.END, "Nenhuma reserva foi feita...")
        
        else:
            with open(BOOKING_FILE) as f:
                content = f.read()
                text_area.insert(tk.END, content)
            
                try:
                    comand = simpledialog.askinteger("Cancelar Reserva", "Insira o slot/hora para cancelar a reserva [8-20]:")

                    if comand is None:
                        return

                    slot_time = time(comand)
                    slot_key = str(f"slot::{current_date}:{slot_time}")

                    with open(rf"{BOOKING_FILE}", "r") as f:
                        content = f.read()
                        if slot_key in content: # confirma se a slot chave se encontra nas reservas do cliente
                            with open(BOOKING_FILE, "r+") as f: 
                                lines = [line for line in f if line.strip() != f'slot::{current_date}:{slot_time}'] # remover o slot cancelado
                                f.seek(0)
                                f.writelines(lines)
                                f.truncate()
                            
                            with open(SCHEDULES_FILE, 'a') as f:
                                f.write(f">> {slot_time}\n")

                            text_area.insert(tk.END, "Reserva cancelada com sucesso!\n")
                            text_area.insert(tk.END, f"{current_date} às {slot_time}\n")

                            if AUDIT_FILE.exists():
                                with open(AUDIT_FILE, "a") as f:
                                    f.write(f"{current_datetime} | CANCEL_SUCCESS | {username} | {slot_key}\n")

                            else:
                                file = open(AUDIT_FILE, "x")
                                with open(AUDIT_FILE, "a") as f:
                                    f.write(f"{current_datetime} | CANCEL_SUCCESS | {username} | {slot_key}\n")

                        else:
                            text_area.insert(tk.END, "Falha no cancelamento - reserva não encontrada\n")

                            with open(AUDIT_FILE, "a") as f:
                                f.write(f"{current_datetime} | CANCEL_FAILED | {username} | {slot_key} - não encontrado ou não reservado\n")

                except ValueError:
                    messagebox.showerror("Erro", "Inserção do slot não é válida!!")
    
    else:
        file = open(BOOKING_FILE, "x")
        text_area.insert(tk.END, "Nenhuma reserva foi feita...")

def view_logs_gui(text_area):
    header = "=" * 8 + " LOGS " + "=" * 8 + "\n"
    if text_area.get(1.0, tk.END).strip() == "":
        text_area.insert(tk.END, header)
    else:
        text_area.insert(tk.END, "\n" + header)
    try:
        if AUDIT_FILE.exists():
            with open(AUDIT_FILE, "a") as f:
                f.write(f"{current_datetime} | LIST_LOGS | SYSTEM | {current_date}\n")

        else:
            file = open(AUDIT_FILE, "x")
            with open(AUDIT_FILE, "a") as f:
                f.write(f"{current_datetime} | LIST_LOGS | SYSTEM | {current_date}\n")

        with open(AUDIT_FILE) as f:
                content = f.read()
                text_area.insert(tk.END, content)

    except FileExistsError:
        text_area.insert(tk.END, "ERRO: audit.tx ou booking.txt não existem...")


def delete_data_gui(text_area):
    header = "Tem a certeza que apagar todos os dados?!?\n"
    if text_area.get(1.0, tk.END).strip() == "":
        text_area.insert(tk.END, header)
    else:
        text_area.insert(tk.END, "\n" + header)
    result = messagebox.askyesno("Confirmação", "Tem a certeza que quer apagar todos os dados?")
    if result:
        if BOOKING_FILE.exists() and AUDIT_FILE.exists():
            text_area.insert(tk.END, "APAGANDO DADOS...\n")
            os.remove(BOOKING_FILE)
            os.remove(AUDIT_FILE)
            text_area.insert(tk.END, "Dados apagados com sucesso!\n")
        else:
            text_area.insert(tk.END, "TODOS OS DADOS JÁ FORAM APAGADOS...\n")
    else:
        text_area.insert(tk.END, "Operação cancelada.\n")


def executar_cliente():
    print("=" * 15 + " CLIENTE " + "=" * 15)
    print("Conexão feita com sucesso...")
    try:
        login()

    except socket.error as error:
        print(f"Erro no Cliente: {error}")

    finally:
        # fecha o socket do cliente (conexão com o servidor)
        cliente.close()
        print("Conexão com o servidor encerrada!!")

executar_cliente()
 