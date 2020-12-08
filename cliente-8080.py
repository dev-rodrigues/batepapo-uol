import socket, pickle, os

# Cria o socket
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket_client.connect((socket.gethostname(), 8082))
except:
    print('ERRO AO CONECTAR COM O SERVIDOR')
    os._exit(1)

def request(message):
    try:
        socket_client.send(message.encode('ascii'))
        received = socket_client.recv(90000)
        response = pickle.loads(received)
        return response
    except:
        print('ERRO AO CONECTAR COM O SERVIDOR')
        os._exit(1)

def opcao_valida(opcao):
    if opcao > 0 and opcao < 5:
        return True
    return False

def escrever_mensagem(response):
    for r in response:
        print(r)

while True:
    print('SELECIONE UMA OPÇÃO')
    print(1, ' - PARA VERIFICAR USUARIOS CONECTADOS')
    print(2, ' - PARA ENVIAR UMA MENSAGEM')
    print(3, ' - LER MENSAGENS')
    print(4, ' - SAIR')

    opcao_selecionada = int(input())
    
    if opcao_valida(opcao_selecionada):
        if opcao_selecionada == 1:
            msg = str(1) + '-'
            response = request(msg)
            escrever_mensagem(response)

        elif opcao_selecionada == 2:
            msg = input('Informe a mensagem: \n')
            msg = str(opcao_selecionada) + '-' + msg
            request(msg)
            os.system('cls' if os.name == 'nt' else 'clear')

        elif opcao_selecionada == 3:
            msg = str(3) + '-'
            response = request(msg)
            escrever_mensagem(response)
          
        else:
            msg = str(4) + '-'
            request(msg)
            os.system('cls' if os.name == 'nt' else 'clear')

socket_client.close()