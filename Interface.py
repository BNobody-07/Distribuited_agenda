import socket
from pathlib import Path
from datetime import date, time, datetime

count = 0
user = ""
current_date = date.today()
current_datetime = datetime.now()

BOOKING_FILE = Path(f"booking{current_date}_{user}.txt")
AUDIT_FILE = Path(f"audit_{user}.txt")
SCHEDULES_FILE = Path("schedules.txt")

def interface():
    while True:
        print("=" * 15, "MENU PRINCIPAL", "=" * 15)
        print('''[1] - Listar slots disponiveis
[2] - Reservar um slot
[3] - Listar minhas reservas
[4] - Cancelar uma reserva 
[5] - Visualizar logs
[6] - Exit
''')
        
        try:
            opcao = int(input("Opção: "))

            match opcao:
                case 1:
                    listar_slots()
                case 2:
                    reservar_slot(user)
                case 3:
                    reservas_user(user)
                case 4:
                    cancelar_reserva(user)
                case 5:
                    view_logs()
                case 6:
                    break
                case _:
                    print("Escolha invalida... TENTE NOVAMENTE")

        except ValueError:
            print("Escolha invalida... TENTE NOVAMENTE")
            interface()

def listar_slots():
    print("=" * 8, "SLOTS DISPONIVEIS", "=" * 8)
    print(f"Slots disponíveis - Data:{current_date}:")
    
    if SCHEDULES_FILE.exists():
        with open(SCHEDULES_FILE) as f:
            print(f.read())
    else:
        file = open(SCHEDULES_FILE, "x")
        with open(SCHEDULES_FILE, "a") as f:
            for x in range(8, 21):
                f.write(f">> {time(x)}")
        
        with open(SCHEDULES_FILE) as f:
            print(f.read())
            f.close()

    if AUDIT_FILE.exists():
        with open(AUDIT_FILE, "a") as f:
            f.write(f"{current_datetime} | LIST_SLOTS | SYSTEM | {current_date}")
    else:
        file = open(AUDIT_FILE, "x")
        with open(AUDIT_FILE, "a") as f:
            f.write(f"{current_datetime} | LIST_SLOTS | SYSTEM | {current_date}")

def reservar_slot(user):
    print("=" * 8, "RERVERSAR SLOTS", "=" * 8)
    try:
        while True:
            comand = int(input("Insira o slot/hora para fazer a reserva [H]: "))

            if comand != type(int):
                print("ERRO: Valor inserido invalido!")
            
            elif comand < 8 or comand >= 21:
                print("ERRO: Slot indisponível neste horário!")

            else:
                break

        slot_time = time(comand)
        slot_key = {f'slot::{current_date}:{slot_time}'}

        slot_time = slot_time.strftime("%X") # Convertes a class datetime/time into a str
        
        with open(rf"{SCHEDULES_FILE}", "r") as f:
            content = f.read()
            if slot_time in content: # verifica se o slot está disponível
                if BOOKING_FILE.exists() and AUDIT_FILE.exists():
                    with open(BOOKING_FILE, "a") as f:
                        f.write(f"{slot_key}")
                        count += 1
                    
                    with open(AUDIT_FILE, "a") as f:
                        f.write(f"{current_datetime} | BOOK_SUCCESS | {user} | {slot_key}")
                else:
                    file = open(BOOKING_FILE, "x")
                    with open(BOOKING_FILE, "a") as f:
                        f.write(f"{slot_key}")

                    file = open(AUDIT_FILE, "x")
                    with open(AUDIT_FILE, "a") as f:
                        f.write(f"{current_datetime} | BOOK_SUCCESS | {user} | {slot_key}")
            
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
                        f.write(f"{current_datetime} | BOOK_FAILED | {slot_key} - ocupado ou indisponível")
            
            interface()

    except ValueError:
        print("ERRO: Inserção do slot não é valida!!")
        interface()

def reservas_user(user):
    print("=" * 8, "MINHAS RESERVAS", "=" * 8)
    try:
        if BOOKING_FILE.exists():
            with open(BOOKING_FILE) as f:
                print(f.read())
        else:
            file = open(BOOKING_FILE, "x")
            with open(BOOKING_FILE, 'r') as f:
                f_char = f.read(0)
            
            if not f_char:
                print("Nenhuma reserva foi feita...")

        if AUDIT_FILE.exists():
            with open("audit.txt", "a") as f:
                f.write(f"{current_datetime} | LIST_USER_BOOKINGS | {user} | count: {count}")
        interface()
    
    except FileNotFoundError:
        print("ERRO: audit.tx ou booking.txt não existem...")
        interface()

def cancelar_reserva(user):
    print("=" * 8, "CANCELAR RESERVA", "=" * 8)
    try:
        # Verifica ficheiro de reservas está vazio
        with open(BOOKING_FILE, 'r') as f:
            f_char = f.read(0)
            
        if not f_char:
            print("Nenhuma reserva foi feita...")
            interface()
        
        else:
            with open(BOOKING_FILE) as f:
                print(f.read())

            while True:
                comand = int(input("Insira o slot/hora para fazer a reserva [H]: "))

                if comand != type(int):
                    print("ERRO: Valor inserido invalido!")
                else:
                    break

            slot_time = time(comand)

            slot_key = str({f'slot::{current_date}:{slot_time}'})
            count -= 1


            with open(rf"{BOOKING_FILE}", "r") as f:
                content = f.read()
                if slot_key in content: # confirma se a slot chave se encontra nas reservas do cliente
                    with open(BOOKING_FILE, "r+") as f: 
                        lines = [line for line in f if line.strip() != f'slot::{current_date}:{slot_time}'] # remover o slot cancelado
                        f.seek(0)
                        f.writelines(lines)
                        f.truncate()
                    
                    with open(SCHEDULES_FILE, 'a') as f:
                        f.write(f">> {slot_time}")
                    
                    print("Reserva cancelada com sucesso!\n")
                    print(f"{current_date} às {slot_time}")

                    if AUDIT_FILE.exists():
                        with open(AUDIT_FILE, "a") as f:
                            f.write(f"{current_datetime} | CANCEL_SUCCESS | {user} | {slot_key}")

                    else:
                        file = open(AUDIT_FILE, "x")
                        with open(AUDIT_FILE, "a") as f:
                            f.write(f"{current_datetime} | CANCEL_SUCCESS | {user} | {slot_key}")

                else:
                    with open(rf"{BOOKING_FILE}", "r") as f:
                        content = f.read()
                        if slot_key not in content:
                            print("Falha no cancelamento - reserva não encontrado\n")

                    with open(AUDIT_FILE, "a") as f:
                        f.write(f"{current_datetime} | CANCEL_FAILED | {user} | {slot_key} - não encontrado ou não reservado")
                                
                interface()

    except ValueError:
        print("ERRO: Inserção do slot não é valida!!")  
        interface()


def view_logs():
    print("=" * 8, "lOGS", "=" * 8)
    try:
        if AUDIT_FILE.exists():
            with open(AUDIT_FILE, "a") as f:
                f.write(f"{current_datetime} | LIST_LOGS | SYSTEM | {current_date}")

        else:
            file = open(AUDIT_FILE, "x")
            with open(AUDIT_FILE, "a") as f:
                f.write(f"{current_datetime} | LIST_LOGS | SYSTEM | {current_date}")

        with open(AUDIT_FILE) as f:
                print(f.read())
        
        interface()

    except FileExistsError:
        print("ERRO: audit.tx ou booking.txt não existem...")
        interface()

# interface()
if __name__ == "__main__":
    print("Interface.py file")
