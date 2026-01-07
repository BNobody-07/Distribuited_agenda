import socket, os
from time import sleep
from pathlib import Path
from datetime import date, time, datetime

current_date = date.today()
current_datetime = datetime.now()

# cria um objeto socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_servidor = "127.0.0.1"  # substitua pelo endereço IP do servidor
porta_servidor = 8888 # substitua pelo número da porta do servidor 

while True:
    global username
    username = input("Digite o ID: ")

    if username == '':
        print("ERRO: Por favor, insira um User ID.")

    elif username.isdigit():
        print("Insira um ID que contenha caracteres...")

    else:
        # estabelece conexão com o servidor
        try: 
            cliente.connect((ip_servidor, porta_servidor))
            cliente.send(username.encode("utf-8")[:1020])
            break

        except ConnectionRefusedError:
            print("ERRO: Nenhuma conexão foi feita porque a maquina alvo rejeitou/não activa.")

BOOKING_FILE = Path(f"booking{current_date}_{username}.txt")
AUDIT_FILE = Path(f"audit_{username}.txt")
SCHEDULES_FILE = Path("schedules.txt")

def interface():
    while True:
        print("=" * 15, "MENU PRINCIPAL", "=" * 15)
        print(f'''[1] - Listar slots disponiveis
[2] - Reservar um slot
[3] - Listar minhas reservas
[4] - Cancelar uma reserva 
[5] - Visualizar logs
[6] - Apagar dados
[7] - Exit
''')
        
        try:
            opcao = int(input("Opção: "))

            match opcao:
                case 1:
                    listar_slots()
                case 2:
                    reservar_slot(username)
                case 3:
                    reservas_user(username)
                case 4:
                    cancelar_reserva(username)
                case 5:
                    view_logs()
                case 6:
                    delete_data()
                case 7:
                    break
                case _:
                    print("Escolha invalida... TENTE NOVAMENTE")

        except ValueError:
            print("Escolha invalida... TENTE NOVAMENTE")
            interface()

def listar_slots():
    print("=" * 8, "SLOTS DISPONIVEIS", "=" * 8)
    print(f"Data:{current_date} - Slots disponíveis:")
    
    if SCHEDULES_FILE.exists():
        with open(SCHEDULES_FILE, 'r') as f:
            f_char = f.read(1)  

        if not f_char:
            with open(SCHEDULES_FILE, "a") as f:
                for x in range(8, 21):
                    f.write(f">> {time(x)}\n")

        with open(SCHEDULES_FILE) as f:
            print(f.read())
    else:
        file = open(SCHEDULES_FILE, "x")
        with open(SCHEDULES_FILE, "a") as f:
            for x in range(8, 21):
                f.write(f">> {time(x)}\n")

        with open(SCHEDULES_FILE) as f:
            print(f.read())
            f.close()

    if AUDIT_FILE.exists():
        with open(AUDIT_FILE, "a") as f:
            f.write(f"{current_datetime} | LIST_SLOTS | SYSTEM | {current_date}\n")
    else:
        file = open(AUDIT_FILE, "x")
        with open(AUDIT_FILE, "a") as f:
            f.write(f"{current_datetime} | LIST_SLOTS | SYSTEM | {current_date}\n")

def reservar_slot(username):
    print("=" * 8, "RERVERSAR SLOTS", "=" * 8)
    try:
        print("Pressione a tecla Enter para não inserir nenhum slot...")
        comand = int(input("Insira o slot/hora para fazer a reserva [H]:"))
            
        if comand < 8 or comand >= 21:
            print("ERRO: Slot indisponível neste horário!")
            reservar_slot(username)

        slot_time = time(comand)
        slot_key = f"slot::{current_date}:{slot_time}"

        slot_time = slot_time.strftime("%X") # Convertes a class datetime/time into a str
        
        with open(rf"{SCHEDULES_FILE}", "r") as f:
            content = f.read()
            if slot_time in content: # verifica se o slot está disponível
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
                    lines = [line for line in f if line.strip() != f">> {slot_time}"] # remover o slot reservado do horario
                    f.seek(0)
                    f.writelines(lines)
                    f.truncate()
                
                print("Reserva realizada com sucesso!")
                print(f"{current_date} às {slot_time}")
            
            else:
                print("Falha na reserva - slot já ocupado ou indisponível!\n")
                with open(AUDIT_FILE, "a") as f:
                        f.write(f"{current_datetime} | BOOK_FAILED | {slot_key} - ocupado ou indisponível\n")
        
        interface()

    except ValueError:
        print("ERRO: Inserção do slot não é valida!!")
        interface()

def reservas_user(username):
    print("=" * 8, "MINHAS RESERVAS", "=" * 8)
    try:
        if BOOKING_FILE.exists():
            with open(BOOKING_FILE) as f:
                print(f.read())
            
            with open(BOOKING_FILE, 'r') as f:
                f_char = f.read(1)
            
            if not f_char:
                print("Nenhuma reserva foi feita...")
        else:
            file = open(BOOKING_FILE, "x")
            with open(BOOKING_FILE) as f:
                print(f.read())
                
            with open(BOOKING_FILE, 'r') as f:
                f_char = f.read(0)
            
            if not f_char:
                print("Nenhuma reserva foi feita...")

        with open(BOOKING_FILE, 'r') as f:
            count = sum(1 for line in f)

        if AUDIT_FILE.exists():
            with open(AUDIT_FILE, "a") as f:
                f.write(f"{current_datetime} | LIST_USER_BOOKINGS | {username} | count: {count}\n")

        interface()
    
    except FileNotFoundError:
        print("ERRO: audit.tx ou booking.txt não existem...")
        interface()

def cancelar_reserva(username):
    print("=" * 8, "CANCELAR RESERVA", "=" * 8)
    # Verifica ficheiro de reservas está vazio
    if BOOKING_FILE.exists():
        with open(BOOKING_FILE, 'r') as f:
            f_char = f.read(1)
            
        if not f_char:
            print("Nenhuma reserva foi feita...")
            interface()
        
        else:
            with open(BOOKING_FILE) as f:
                print(f.read())
            
                try:
                    print("Pressione a tecla Enter para não inserir nenhum slot...")
                    comand = int(input("Insira o slot/hora para fazer a reserva [H]:"))

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

                            print("Reserva cancelada com sucesso!")
                            print(f"{current_date} às {slot_time}")

                            if AUDIT_FILE.exists():
                                with open(AUDIT_FILE, "a") as f:
                                    f.write(f"{current_datetime} | CANCEL_SUCCESS | {username} | {slot_key}\n")

                            else:
                                file = open(AUDIT_FILE, "x")
                                with open(AUDIT_FILE, "a") as f:
                                    f.write(f"{current_datetime} | CANCEL_SUCCESS | {username} | {slot_key}\n")

                        else:
                            with open(rf"{BOOKING_FILE}", "r") as f:
                                content = f.read()
                                if slot_key not in content:
                                    print("Falha no cancelamento - reserva não encontrado\n")

                            with open(AUDIT_FILE, "a") as f:
                                f.write(f"{current_datetime} | CANCEL_FAILED | {username} | {slot_key} - não encontrado ou não reservado\n")
                                        
                    interface()

                except ValueError:
                    print("ERRO: Inserção do slot não é valida!!")  
                    interface()
    
    else:
        file = open(BOOKING_FILE, "x")
        cancelar_reserva(username)

def view_logs():
    print("=" * 8, "lOGS", "=" * 8)
    try:
        if AUDIT_FILE.exists():
            with open(AUDIT_FILE, "a") as f:
                f.write(f"{current_datetime} | LIST_LOGS | SYSTEM | {current_date}\n")

        else:
            file = open(AUDIT_FILE, "x")
            with open(AUDIT_FILE, "a") as f:
                f.write(f"{current_datetime} | LIST_LOGS | SYSTEM | {current_date}\n")

        with open(AUDIT_FILE) as f:
                print(f.read())
        
        interface()

    except FileExistsError:
        print("ERRO: audit.tx ou booking.txt não existem...")
        interface()


def delete_data():
    print("\nTem a certeza que apagar todos os dados?!?")
    while True:
        try:
            comand = input("[S] ou [N]: ").upper()

            if comand == "S":
                
                if BOOKING_FILE.exists() and AUDIT_FILE.exists():
                    print("APAGANDO DADOS...")
                    os.remove(BOOKING_FILE)
                    os.remove(AUDIT_FILE)
                    
                else:
                    print("TODOS OS DADOS JÁ FORAM APAGADOS...\n")

            elif comand == "N":
                print("Retornando ao menu principal...\n")
            
            else:
                print("Opção invalida... TENTE NOVAMENTE!")
                delete_data()

            sleep(2)
            interface()

        except ValueError:
            print("Nenhuma opção foi selecionada...")
            interface()


def executar_cliente():
    print("=" * 15 + " CLIENTE " + "=" * 15)
    print(f"""Conexão feita com sucesso...
[close] - Encerrar servidor""")
    try:
        while True:
            interface()
            print("\nDigite \"close\" para encerrar a conexão com o servidor")
            print("Digite \"iniciar\" para voltar a conexão com o servidor")
            mensagem = input()
        
            # se cliente digitar "closed", encerramos o loop e fechamos o socket
            if mensagem.lower() == "close":
                break
            
            elif mensagem.lower() == "iniciar":
                interface()
            
            else:
                while True:
                    print("ERRO: Comando inserido não é valido... TENTE NOVAMENTE.")
                    print("\nDigite \"close\" para encerrar a conexão com o servidor")
                    print("Digite \"iniciar\" para voltar a conexão com o servidor")
                    mensagem = input()

                    if mensagem.lower() == "close":
                        break
                        
                    elif mensagem.lower() == "iniciar":
                        break

            #cliente.send(mensagem.encode("utf-8")[:1024])

    except socket.error as error:
        print(f"Erro no Cliente: {error}")
    
    finally:
        # fecha o socket do cliente (conexão com o servidor)
        cliente.close()
        print("Conexão com o servidor encerrada!!")

executar_cliente()
 