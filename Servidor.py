import socket

# Cria um objeto socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configurações do servidor
ip_servidor = "127.0.0.1"  # Substitua pelo IP desejado
porta = 8888

print("=" * 15 + " SERVIDOR " + "=" * 15)

# Associa o socket ao IP e à porta
servidor.bind((ip_servidor, porta))
servidor.listen(3)  # Define o número máximo de conexões pendentes
print(f"Servidor iniciado e aguardando conexões em: {ip_servidor}:{porta}")

# Aguarda uma conexão de cliente e o seu username
socket_cliente, endereco_cliente = servidor.accept()

global username_cliente
username_cliente = socket_cliente.recv(1020).decode("utf-8")

print(f"Conexão aceita de {endereco_cliente[0]}:{endereco_cliente[1]}")
print(f"ID do User: {username_cliente}")

def executar_servidor():
    try:
        while True:
            try:
                # Recebe dados do cliente
                requisicao = socket_cliente.recv(1024).decode("utf-8") # Converte bytes para string
                
                if not requisicao:
                    print("Cliente desconectado.")
                    break

                # Encerra conexão se o cliente enviar "close"
                if requisicao.lower() == "close":
                    socket_cliente.send("Conexão encerrada pelo servidor.".encode("utf-8"))
                    print("Encerrando conexão com o cliente...")
                    break
                else:
                    break
               
            except socket.error as e:
                print(f"Erro ao processar a solicitação: {e}")
                break

        # Fecha o socket de conexão com o cliente
        socket_cliente.close()
        print("\nConexão com o cliente encerrada!!")

    except socket.error as e:
        print(f"Erro no servidor: {e}")

    finally:
        # Fecha o socket do servidor
        servidor.close()
        print("Servidor encerrado...")

# executar_servidor()
