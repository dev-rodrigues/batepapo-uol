import socket, pickle, threading, os
from datetime import datetime
# luiz.maia@prof.infnet.edu.br

os.system('cls' if os.name == 'nt' else 'clear')
print('BATE PAPO DA UOL ONLINE')

porta = 8080
host  = "192.168.0.12"

pool = {
  'connections': [],
  'posts': [],
}

def criar_conexao():
  global porta, host, pool

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
    socket_server.bind((host, porta))
    socket_server.listen()    
    print("Servidor de nome:", host, " - Aguardando conexão na porta:", porta)

    conexao, ender = socket_server.accept()
    
  pool['connections'].append([conexao, socket_server, False, ender])

def get_response():
  response = []
  for post in pool['posts']:
    response.append(post.to_map())

  return response

def remove_connection(host, port):
  for n in range(0, len(pool['connections'])):
    if pool['connections'][n][3] == host and pool['connections'][n][4] == port:
      del(pool['connections'][n])

def get_request_send_response(client, server, host, port):
  while True:
    msg = ''
    decode = ''
    response = 'NoNe'

    try:
      msg = client.recv(5000)
      decode = msg.decode('ascii')
    except:
      print('UNEXPECTED ERROR, CONNECTION BROKEN')
      remove_connection(host, port)
      break

    request = decode.split('-')

    try:
      if int(request[0]) == 4:
        break
    
      elif int(request[0]) == 1:
        connections = pool['connections']

        response = []
        for connection in connections:
          conn = connection[3]
          response.append(conn)

      elif int(request[0]) == 2:
        post = Post(request[1], host, port)
        pool['posts'].append(post)
        response = 'OK'

      elif int(request[0]) == 3:
        response = get_response()
    except:
      print('conexão com o cliente na porta: ', port, ' fechada')
      break
    
    bytes_resp = pickle.dumps(response)
    
    client.send(bytes_resp)

  client.close()
  server.close()

class ThreadConnection(threading.Thread):
  def __init__(self, threadID, name, counter):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.counter = counter

  def run(self):
    while True:
      criar_conexao()
      print ("Connection Established")

class ThreadCommunication(threading.Thread):
  def __init__(self, threadID, name, counter, server_, client_, host_, port_):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.counter = counter
    self.server_ = server_
    self.client_ = client_
    self.host_ = host_
    self.port_ = port_

  def run(self):       
    get_request_send_response(self.client_, self.server_, self.host_, self.port_)

class Post:
  def __init__(self, msg, host_, port_):
    self.datetime = str(datetime.now())
    self.msg = msg
    self.host_ = host_
    self.port_ = port_
  
  def to_map(self):
    return {
      'datetime': self.datetime,
      'msg': self.msg,
      'host': self.host_,
      'port': self.port_
    }

t = ThreadConnection(1, 'ThreadConnection', 1)
t.start()

while True:
  for connection in pool['connections']:
    connected = connection[2]
    host = connection[3][0]
    port = connection[3][1]

    if not connected:
      server = connection[1]
      client = connection[0]

      connection[2] = True
      t2 = ThreadCommunication(2, 'ThreadCommunication', 1, server, client, host, port)
      t2.start()
