import socket
sock = socket.socket()

sock.connect(('localhost', 9090)) #коннектимся через порт 9090
while True:
    message=str(input())
    message=bytes(message, encoding='utf-8')
    sock.send(message) #отправляем сообщение
    data = sock.recv(1024) #получаем данные от сервера
    print(data) #выдаем на экран полученный ответ
    if (message==bytes("quit", encoding='utf-8')):
        print("Bye!")
        break

sock.close() #закрываем соединение
