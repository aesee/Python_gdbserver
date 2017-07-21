# -- coding: cp1251 --
import socket

switch = { '$qSupported':'swbreak+;PacketSize=131072', #119?
           '$vMustReplyEmpty':'',
           '$Hg0':'OK',
           #'$Hg0':'',
           '$Hg-1':'Ok',
           #'$qTStatus':'T1',
           '$qTStatus':'',
           #'+$S05':'S05',
           '$qfThreadInfo':'m 0',
           #'$qfThreadInfo':'',
           '$qsThreadInfo':'l',
           '$Hc-1':'OK',
           #'$Hc-1':'',
           '$qC':'',
           '$qAttached':'1',
           #'$qAttached':'',
           '$qOffsets':'Text=00;Data=00;Bss=0',
           #'$qOffsets':'',
           #'$g#67':'xxxxxxxx00000000xxxxxxxx00000000',
           '$g#67':'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 
           #'$p20':'00',
           '$p20':'0010000000000000',
           '$qSymbol':'',
           '$vKill':'Ok',
           '+$?':'S00',
           #'$?':'S05',
           '$qTfV':'',
           '$qTsP':'',
           #'$qL12':'',
           '$qL12':'0x0000000000001000 in ?? ()',
           'vCont?':'vCont;c',
           #'$m':'12345',
            }

def Checksum(data):
    checksum = 0
    for c in data:
        checksum += ord(c)
    #return hex(checksum)[-2:]
    return checksum & 0xff

def ReadMemory(data):
    return "2f86"

def ReadRegisters(data):
    return "123456789abcdef0"

def WriteRegisters(data):
    return "Ok"

def WriteRegisterN(data):
    return "Ok"

def WriteMemory(data):
    return "Ok"

def LastSignal(data):
    return "S00"

def Step():
    return LastSignal("OK")

def Continue():
    return LastSignal("OK")

def Message(data):
    if (data.find('$m') != -1):
        return ReadMemory(data)
    elif (data.find('$g') != -1):
        return ReadRegisters(data)
    elif (data.find('$G') != -1):
        return WriteRegisters(data)
    elif (data.find('$P') != -1):
        return WriteRegisterN(data)
    elif (data.find('$M') != -1):
        return WriteMemory(data)
    elif (data.find('$?') != -1):
        return LastSignal(data)
    elif (data.find('$s') != -1):
        return Step() 
    elif (data.find('$c') != -1):
        return Continue()
    else:
        for key in switch:
#        if data.startswith(key,2):
            if (data.find(key) != -1):
                return switch[key]
    return 'Ok'
#    return switch[i]

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
        data = ''
        pastData = ''
        ##получаем от клиента по 1кб информации в цикл,
        ##пока клиент не закончит слать информацию
        while True:
            pastData=data
            while (data==pastData):
                data = str(conn.recv(1024).decode('cp1251'))
            log.write(data)
            log.write("\n")
            print("Received: ", data)
            msg=Message(data)
            cs=Checksum(msg)
            try:
                self.send(msg)
                print("Sending: ", msg)
            except Exception:
                print("Client is not answering.")
            log.write("+$"+str(msg)+"#"+str(cs)[-2:])
            log.write("\n")

        ##закрываем соединение
        print("Bye!")
        self.netout.close()
        self.clientsocket.close()
        log.close()
        conn.close()

#sock = socket.socket()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

##устанавливаем связь с клиентом
#port = 3333
#sock.bind(('',port))
sock.bind(('',3333)) ##связываем сокет с хостом и портом
sock.listen(1) ## максимальное количество подключений в очереди
conn, addr = sock.accept() ##принимаем новый сокет и адрес клиента
GDBClientHandler(conn).run()

#############################################################
#def qL12():   
