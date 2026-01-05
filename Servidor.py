from socket import socket
from datetime import date, time;

# current_date = date.today()
# horarios = [8, 10, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
# reservas = []

# Cria um objeto socket
servidor = socket(socket.AF_INET, socket.SOCK_STREAM)

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
        # Loop para receber e responder mensagens
        while True:
            try:
                # Recebe dados do cliente
                requisicao = socket_cliente.recv(1024).decode("utf-8") # Converte bytes para string
                
                if not requisicao:
                    print("Cliente desconectado.")
                    break
                
                # Envia resposta ao cliente
                # resposta = "mensagem recebida e aceita."
                # socket_cliente.send(resposta.encode("utf-8")[:1028])

                # Encerra conexão se o cliente enviar "close"
                if requisicao.lower() == "close":
                    socket_cliente.send("Conexão encerrada pelo servidor.".encode("utf-8"))
                    print("Encerrando conexão com o cliente...")
                    break
                else:
                    # Recebe a mensagem do cliente
                    break
                   
                # Envia mensagem ao cliente
               
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
