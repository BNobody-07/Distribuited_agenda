# Sistema de Agenda Distribuído

Um sistema distribuído de agendamento de compromissos (Serviços/Consultas) construído em Python, apresentando uma interface gráfica do usuário (GUI) para clientes e um servidor multi-threaded que lida com reservas concorrentes enquanto previne reservas duplicadas.

## Funcionalidades

- **GUI do Cliente**: Interface intuitiva baseada em Tkinter para interação fácil
- **Suporte Multi-cliente**: O servidor lida com múltiplas conexões simultâneas usando threading
- **Prevenção de Reserva Concorrente**: Operações thread-safe previnem reservas duplicadas de slots
- **Gerenciamento de Slots em Tempo Real**: Verificação e atualizações dinâmicas de disponibilidade
- **Registro de Auditoria**: Registro abrangente de todas as ações do usuário
- **Gerenciamento de Dados**: Visualizar, cancelar e excluir reservas e logs

## Arquitetura

- **Servidor (Servidor.py)**: Servidor de socket multi-threaded gerenciando dados de slots compartilhados com bloqueios de sincronização
- **Cliente (Cliente.py)**: Aplicação GUI conectando ao servidor para operações de reserva
- **Armazenamento de Dados**: Rastreamento de slots em memória com logs de auditoria baseados em arquivo por usuário

## Requisitos

- Python 3.x
- Tkinter (geralmente incluído com instalações Python)

## Instalação

1. Clone ou baixe os arquivos do projeto
2. Certifique-se de que Python 3.x está instalado
3. Nenhuma dependência adicional necessária (Tkinter é padrão)

## Uso

### Iniciando o Servidor

```bash
python Servidor.py
```

O servidor começará a ouvir em localhost:8888 e exibirá confirmações de conexão.

### Executando a GUI do Cliente

```bash
python Cliente.py
```

Ou no Windows:

```bash
start python Cliente.py
```

### Demonstração de Prevenção de Reserva Concorrente

1. Inicie o servidor em um terminal
2. Lance duas instâncias da GUI do cliente
3. Conecte cada cliente com nomes de usuário diferentes (ex.: "user1", "user2")
4. Ambos os clientes tentam reservar o mesmo slot simultaneamente
5. Observe que apenas uma reserva é bem-sucedida; o segundo recebe uma mensagem de erro

## Operações Disponíveis

- **Listar Slots**: Visualizar todos os slots de tempo disponíveis (8:00 a 20:00)
- **Reservar Slot**: Reservar um slot de tempo específico
- **Visualizar Reservas**: Ver suas reservas atuais
- **Cancelar Reserva**: Remover uma reserva existente
- **Visualizar Logs**: Exibir histórico de auditoria
- **Excluir Dados**: Limpar todos os dados do usuário e logs

## Detalhes Técnicos

- **Threading**: O servidor usa threading.Lock para sincronização
- **Comunicação por Socket**: Sockets TCP para interação cliente-servidor
- **Estruturas de Dados**: Listas para slots disponíveis, dicionários para reservas de usuários
- **Tratamento de Erros**: Mensagens de erro abrangentes e gerenciamento de conexão

## Arquivos

- `Servidor.py`: Implementação do servidor multi-threaded
- `Cliente.py`: Aplicação cliente GUI
- `README.md`: Este arquivo de documentação

## Licença

Este projeto é open-source e disponível sob a Licença MIT.
