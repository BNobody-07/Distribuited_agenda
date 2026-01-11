import socket
import threading
import time
from datetime import date, time, datetime

# Configurações do servidor
ip_servidor = "127.0.0.1"
porta = 8080

current_date = date.today()
current_datetime = datetime.now()

# Dados compartilhados
available_slots = [time(hour) for hour in range(8, 21)]  # Slots de 8:00 a 20:00
lock = threading.Lock()

def get_booking_filename(username):
    return f"booking{current_date}_{username}.txt"

def load_user_bookings(username):
    filename = get_booking_filename(username)
    try:
        with open(filename, "r") as f:
            slots = [datetime.strptime(line.strip(), "%H:%M:%S").time() for line in f if line.strip()]
        return slots
    except FileNotFoundError:
        return []

def save_user_bookings(username, slots):
    filename = get_booking_filename(username)
    with open(filename, "w") as f:
        for slot in sorted(slots):
            f.write(f"{slot.strftime('%H:%M:%S')}\n")


# Recebe os pedidos vindo dos Clientes
def handle_client(client_socket, address, username):
    print(f"Conexão aceita de {address[0]}:{address[1]} - User: {username}")
    try:
        while True:
            request = client_socket.recv(1024).decode("utf-8")
            if not request:
                break
            if request.lower() == "close":
                client_socket.send("Conexão encerrada.".encode("utf-8"))
                break

            response = process_request(request, username)
            client_socket.send(response.encode("utf-8"))

    except Exception as e:
        print(f"Erro com cliente {username}: {e}")
    finally:
        client_socket.close()
        print(f"Conexão com {username} encerrada.")

# Processa os pedidos vindo dos Clientes
def process_request(request, username):
    global available_slots
    parts = request.split("|")
    command = parts[0].upper()

    with lock:
        # Listar os slots
        if command == "LIST":
            slots_str = "\n".join([f">> {slot.strftime('%H:%M:%S')}" for slot in available_slots])
            
            # Registra a listagem no ficheiro texto "audit_nome do utilizador"
            with open(f"audit_{username}.txt", "a") as f:
                    f.write(f"{current_datetime} | LIST_SLOTS | SYSTEM | {current_date}\n")
            
            return f"\n📅 Slots disponíveis:\n{slots_str}"
        

        # Reservar os slot/hora
        elif command == "BOOK":
            if len(parts) < 2:
                return "Erro: Hora não fornecida."
            try:
                hour = int(parts[1])
                slot_time = time(hour)

                # Verifica se o slot/hora está disponivel na lista de slots disponiveis
                if slot_time not in available_slots:

                    with open(f"audit_{username}.txt", "a") as f:
                        f.write(f"{current_datetime} | BOOK_FAILED | {username} | slot::{current_date}:{slot_time} - already booked\n")

                    return f"❌ Slot indisponível ou já reservado."
                
                # Remove o slot/hora quando for reservado
                available_slots.remove(slot_time)

                user_bookings = load_user_bookings(username)
                user_bookings.append(slot_time)
                save_user_bookings(username, user_bookings)

                # Log da reserva
                with open(f"audit_{username}.txt", "a") as f:
                    f.write(f"{current_datetime} | BOOK_SUCCESS | {username} | slot::{current_date}:{slot_time}\n")
                return f"\n✅ Reserva realizada: {current_date} às {slot_time.strftime('%H:%M:%S')}"
            
            except ValueError:
                return "Hora inválida."

        # Lista as reservas realizadas pelo user
        elif command == "VIEW":
            user_bookings = load_user_bookings(username)

            # Verifica se as reservas está vazia
            if not user_bookings:
                with open(f"audit_{username}.txt", "a") as f:
                    f.write(f"{current_datetime} | LIST_USER_BOOKINGS | {username} | count:{len(user_bookings)}\n")

                return "❌ Nenhuma reserva feita."

            bookings_str = "\n".join([f"slot::{current_date}:{slot.strftime('%H:%M:%S')}" for slot in user_bookings])

            with open(f"audit_{username}.txt", "a") as f:
                    f.write(f"{current_datetime} | LIST_USER_BOOKINGS | {username} | count:{len(user_bookings)}\n")

            return f"\nSuas reservas:\n{bookings_str}"

        # Processo responsavel por cancelar as reservas
        elif command == "CANCEL":
            # Verifica se o input está vazio
            if len(parts) < 2:
                return "Erro: Hora não fornecida."
            try:
                hour = int(parts[1])
                slot_time = time(hour)

                user_bookings = load_user_bookings(username)

                # Verifica se existe uma reserva há ser cancelada
                if slot_time not in user_bookings:
                    with open(f"audit_{username}.txt", "a") as f:
                        f.write(f"{current_datetime} | CANCEL_FAILED | {username} | slot::{current_date}:{slot_time} - not found\n")
                    return "❌ Reserva não encontrada."

                # remove o slot e o retorna como disponivel
                user_bookings.remove(slot_time)
                save_user_bookings(username, user_bookings)
                available_slots.append(slot_time)
                available_slots.sort()

                # Log de cancelamento
                with open(f"audit_{username}.txt", "a") as f:
                    f.write(f"{current_datetime} | CANCEL_SUCCESS | {username} | slot::{current_date}:{slot_time}\n")
                return f"\n✅ Reserva cancelada: {current_date} às {slot_time.strftime('%H:%M:%S')}"

            except ValueError:
                return "Hora inválida."

        elif command == "LOGS":
            try:
                # Listar os logs 
                with open(f"audit_{username}.txt", "r") as f:
                    logs = f.read()
                return logs if logs else "Nenhum log."
            except FileNotFoundError:
                return "Arquivo de log não encontrado."

        elif command == "DELETE":
            try:
                import os
                booking_file = get_booking_filename(username)
                if os.path.exists(booking_file):
                    os.remove(booking_file)
                os.remove(f"audit_{username}.txt")
            except FileNotFoundError:
                pass
            return "✅ Dados apagados."
        
        else:
            return "Comando inválido."

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((ip_servidor, porta))
    servidor.listen(5)
    print("=" * 15 + " SERVIDOR " + "=" * 15)
    print(f"Servidor iniciado em {ip_servidor}:{porta}")

    # Load existing bookings to update available_slots
    import os
    for file in os.listdir('.'):
        if file.startswith('booking') and file.endswith('.txt'):
            username = file.split('_')[1].split('.')[0]
            slots = load_user_bookings(username)
            for slot in slots:
                if slot in available_slots:
                    available_slots.remove(slot)

    try:
        while True:
            client_socket, address = servidor.accept()
            username = client_socket.recv(1024).decode("utf-8")
            threading.Thread(target=handle_client, args=(client_socket, address, username)).start()

    except KeyboardInterrupt:
        print("Servidor encerrado.")

if __name__ == "__main__":
    main()
