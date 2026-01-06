from pathlib import Path
from datetime import date, time, datetime
from Cliente import username

count = 0
# user = username
current_date = date.today()
current_datetime = datetime.now()

BOOKING_FILE = Path("booking.txt")
AUDIT_FILE = Path("audit.txt")
SCHEDULES_FILE = Path("schedules.txt")

def interface():
    while True:
        print("\n")
        print("=" * 15, "MENU PRINCIPAL", "=" * 15)
        print('''[1] - Listar slots disponiveis
[2] - Reservar um slot
[3] - Cancelar uma reserva 
[4] - Listar minhas reservas
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
                    view_logs(user)
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
            print(f.read().splitlines())
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
        comand = input("Insira o slot para fazer a reserva [H]: ")
        slot_time = time(comand)

        confirm = {f'slot::{current_date}:{slot_time}'}

        if comand in f:
            print("Reserva realizada com sucesso!")
            print(f"{current_date} às {slot_time}")
            count += 1

            if BOOKING_FILE.exists() and AUDIT_FILE.exists():
                with open(BOOKING_FILE, "a") as f:
                    f.write(f"{confirm}")
                
                with open(AUDIT_FILE, "a") as f:
                    f.write(f"{current_datetime} | BOOK_SUCCESS | {user} | {confirm}")

        else:
            print("Falha na reserva - slot já ocupado ou indisponível\n")

    except (ValueError, IndexError):
        print("Nehuma reserva foi feita...")
        interface()

def reservas_user(username):
    print("=" * 8, "MINHAS RESERVAS", "=" * 8)
    try:
        if BOOKING_FILE.exists():
            with open(BOOKING_FILE) as f:
                print(f.read())
        else:
            file = open(BOOKING_FILE, "x")
            with open(BOOKING_FILE, 'r') as f:
                f_char = f.read(1)
            
            if not f_char:
                print("Nenhuma reserva foi feita...")

        if AUDIT_FILE.exists():
            with open("audit.txt", "a") as f:
                f.write(f"{current_datetime} | LIST_USER_BOOKINGS | {user} | count: {count}")

    except FileNotFoundError:
        print("ERRO: AUDIT or BOOKING FILE DOESN'T EXIST...")
        interface()

def cancelar_reserva():
    print("=" * 8, "CANCELAR RESERVA", "=" * 8)
    try:
        comand = input("Insira o slot para cancelar a reserva: ")
        comand2 = input("Digite a hora do slot que cancelou [H]: ")
        slot_time = time(comand2)

        confirm = {f'slot::{current_date}:{slot_time}'}
        count -= 1
        
        if AUDIT_FILE.exists():
            with open(AUDIT_FILE, "a") as f:
                f.write(f"{current_datetime} | CANCEL_SUCCESS | {user} | {confirm}")

    except FileNotFoundError:
        print("Nehuma reserva para ser cancelada...")
        interface()


def view_logs(username):
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
        print("ERRO: AUDIT or BOOKING FILE DOESN'T EXIST...")
        interface()

# interface()
