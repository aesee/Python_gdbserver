# -- coding: cp1251 --

import socket

switch = { 1:'PacketSize=119',
           2:'',
           3:'OK',
           4:'', #'T0;tnotrun:0',
           5:'S05',
           6:'m 0',
           7:'l',#'1000',
           8:'OK',
           9:'QC-1',#"QC '0'",
           10:'1',
           11:'Text=0;Data=0;Bss=0', #'xxxxxxxx00000000xxxxxxxx00000000',#'Text=0333e564;Data=0;Bss=0333e564;',
           12:'xxxxxxxx00000000xxxxxxxx00000000',
           13:'00',
           14:'m 0',
           15:'l',
           16:'stub' }

def Checksum(data):
    checksum = 0
    for c in data:
        checksum += ord(c)
    #return hex(checksum)[-2:]
    return checksum & 0xff

#пока что data не используется
def Message(i):
    #return "OK"
    #return "PacketSize=3ff;qXfer:features:read+"
    #return "qfThreadInfo"
    return switch[i]

class GDBClientHandler(object):
    def __init__(self, clientsocket):
        self.clientsocket = clientsocket
        self.netin = clientsocket.makefile('r')
        self.netout = clientsocket.makefile('w')
        self.last_pkt = None

    def send(self, msg):
        self.send_raw('+$%s#%.2x' % (msg, Checksum(msg)))
    def send_raw(self, r):
        self.netout.write(r)
        self.netout.flush()
    
    def run(self):
        print("connected:", addr)
        log = open("log.txt", 'w')
        msg, cs = "",""
        i = 0
        data = ''
        pastData = ''
        ##получаем от клиента по 1кб информации в цикл,
        ##пока клиент не закончит слать информацию
        while True:
            #while (data=="b''"):
            data = str(conn.recv(1024))
            log.write(data)
            log.write("\n")
            print("Received: ", data)
            i+=1
            msg=Message(i)
            cs=Checksum(msg)
            try:
                #if (data!="b''"):
                self.send(msg)
                ##tosend="+$"+str(msg)+"#"+str(cs)
                ##conn.send(bytes(tosend, encoding='utf-8'))
            except Exception:
                print("Client is not answering.")
            log.write("+$"+str(msg)+"#"+str(cs)[-2:])
            log.write("\n")
            if (i > 15):
                while True:
                    pastData=data
                    while (data==pastData):                    
                        data = str(conn.recv(1024))
                    log.write(data)
                    log.write("\n")
                    print("Received: ", data)
                    msg="OK"
                    cs=Checksum(msg)
                    self.send(msg)
        ##закрываем соединение
        print("Bye!")
        self.netout.close()
        self.clientsocket.close()
        log.close()
        conn.close()

#sock = socket.socket()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

##устанавливаем связь с клиентом
#port = 9090
#sock.bind(('',port))
sock.bind(('',3333)) ##связываем сокет с хостом и портом
sock.listen(1) ## максимальное количество подключений в очереди
conn, addr = sock.accept() ##принимаем новый сокет и адрес клиента
GDBClientHandler(conn).run()
