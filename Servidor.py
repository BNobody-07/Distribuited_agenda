import socket
import threading

# Cria um objeto socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configurações do servidor
ip_servidor = "127.0.0.1"  # Substitua pelo IP desejado
porta = 8888

print("=" * 15 + " SERVIDOR " + "=" * 15)

# Associa o socket ao IP e à porta
servidor.bind((ip_servidor, porta))
servidor.listen(5)  # Define o número máximo de conexões pendentes
print(f"Servidor iniciado e aguardando conexões em: {ip_servidor}:{porta}")

def handle_client(socket_cliente, endereco_cliente):
    try:
        # Recebe o username do cliente
        username_cliente = socket_cliente.recv(1020).decode("utf-8")
        print(f"Conexão aceita de {endereco_cliente[0]}:{endereco_cliente[1]}")
        print(f"ID do User: {username_cliente}")

        while True:
            try:
                # Recebe dados do cliente
                requisicao = socket_cliente.recv(1024).decode("utf-8")  # Converte bytes para string

                if not requisicao:
                    print(f"Cliente {username_cliente} desconectado.")
                    break

                # Encerra conexão se o cliente enviar "close"
                if requisicao.lower() == "close":
                    socket_cliente.send("Conexão encerrada pelo servidor.".encode("utf-8"))
                    print(f"Encerrando conexão com o cliente {username_cliente}...")
                    break
                else:
                    # Aqui você pode processar outras requisições se necessário
                    pass

            except socket.error as e:
                print(f"Erro ao processar a solicitação do cliente {username_cliente}: {e}")
                break

    except socket.error as e:
        print(f"Erro no cliente {endereco_cliente}: {e}")

    finally:
        # Fecha o socket de conexão com o cliente
        socket_cliente.close()
        print(f"\nConexão com o cliente {username_cliente} encerrada!!")

def executar_servidor():
    try:
        while True:
            # Aguarda uma conexão de cliente
            socket_cliente, endereco_cliente = servidor.accept()
            # Cria uma nova thread para lidar com o cliente
            client_thread = threading.Thread(target=handle_client, args=(socket_cliente, endereco_cliente))
            client_thread.start()

    except KeyboardInterrupt:
        print("Servidor interrompido pelo usuário.")

    finally:
        # Fecha o socket do servidor
        servidor.close()
        print("Servidor encerrado...")

executar_servidor()
