import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import date, datetime

current_date = date.today()
current_datetime = datetime.now()

ip = "127.0.0.1"
port = 8080

class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reservas - Cliente")
        self.client_socket = None
        self.username = ""

        # Username input
        tk.Label(root, text="Digite o ID do usuário:").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)
        tk.Button(root, text="Conectar", command=self.connect_to_server).pack(pady=5)

        # Area de resposta
        self.response_text = scrolledtext.ScrolledText(root, width=50, height=10)
        self.response_text.pack(pady=10)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Listar Slots", command=self.list_slots).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Reservar Slot", command=self.book_slot).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Ver Reservas", command=self.view_bookings).grid(row=1, column=0, padx=5)
        tk.Button(button_frame, text="Cancelar Reserva", command=self.cancel_booking).grid(row=1, column=1, padx=5)
        tk.Button(button_frame, text="Ver Logs", command=self.view_logs).grid(row=2, column=0, padx=5)
        tk.Button(button_frame, text="Apagar Dados", command=self.delete_data).grid(row=2, column=1, padx=5)
        tk.Button(button_frame, text="Sair", command=self.exit_app).grid(row=3, column=0, columnspan=2, pady=5)

        # Slot input
        tk.Label(root, text="Hora do slot (8-20):").pack(pady=5)
        self.slot_entry = tk.Entry(root)
        self.slot_entry.pack(pady=5)

    # Função para conecer com o servidor 
    def connect_to_server(self):
        username = self.username_entry.get().strip()
        if not username or username.isdigit():
            messagebox.showerror("Erro", "Insira um ID válido (não apenas números).")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, port))
            self.client_socket.send(username.encode("utf-8"))
            self.username = username
            self.response_text.insert(tk.END, f"✅ Conectado como {username}\n")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na conexão: {e}")

    # Envio de pedidos ao servidor, para obter a resposta do processo
    def send_request(self, request):
        # Apresenta um erro caso o Cliente não se conecte
        if not self.client_socket:
            messagebox.showerror("Erro", "Não conectado ao servidor.")
            return None
        try:
            # Envia e recebe os pedidos
            self.client_socket.send(request.encode("utf-8"))
            response = self.client_socket.recv(4096).decode("utf-8")
            return response
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na comunicação: {e}")
            return None

    # Listar slots
    def list_slots(self):
        response = self.send_request("LIST")
        if response:
            self.response_text.insert(tk.END, response + "\n")

    # Reservar slots
    def book_slot(self):
        slot = self.slot_entry.get().strip()
        if not slot.isdigit():
            messagebox.showerror("Erro", "Insira uma hora válida.")
            return
        response = self.send_request(f"BOOK|{slot}")
        if response:
            self.response_text.insert(tk.END, response + "\n")

    # Ver reservas
    def view_bookings(self):
        response = self.send_request("VIEW")
        if response:
            self.response_text.insert(tk.END, "=" * 12 + " RESERVAS " + "=" * 12)
            self.response_text.insert(tk.END, response + "\n")

    # Cancelar Reservas
    def cancel_booking(self):
        slot = self.slot_entry.get().strip()
        if not slot.isdigit():
            messagebox.showerror("Erro", "Insira uma hora válida.")
            return
        response = self.send_request(f"CANCEL|{slot}")
        if response:
            self.response_text.insert(tk.END, response + "\n")

    # Listar logs
    def view_logs(self):
        response = self.send_request("LOGS")
        if response:
            self.response_text.insert(tk.END, "=" * 12 + " LOGS " + "=" * 12 + "\n")
            self.response_text.insert(tk.END, response + "\n")

    # Apagar todos os dados do utilizador
    def delete_data(self):
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja apagar todos os dados?"):
            response = self.send_request("DELETE")
            if response:
                self.response_text.insert(tk.END, response + "\n")

    def exit_app(self):
        if self.client_socket:
            self.send_request("close")
            self.client_socket.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientGUI(root)
    root.mainloop()
 