import socket
from Interface import interface

# cria um objeto socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_servidor = "127.0.0.1"  # substitua pelo endereço IP do servidor
porta_servidor = 8888 # substitua pelo número da porta do servidor 

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
            executar_cliente()
            break

        except ConnectionRefusedError:
            print("ERRO: Nenhuma conexão foi feita porque a maquina alvo rejeitou/não activa.")


 