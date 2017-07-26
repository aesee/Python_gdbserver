# -- coding: cp1251 --
import socket

switch = { #'$qSupported':'swbreak+;PacketSize=131072', #119?   131072
           '$qSupported':'PacketSize=131072',
           '$vMustReplyEmpty':'',
           '$Hg0':'OK',
           #'$Hg0':'',
           '$Hg-1':'Ok',
           #'$qTStatus':'T1',
           '$qTStatus':'',
           #'+$S05':'S05',
           '$qfThreadInfo':'m0',
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
           #'vCont?':'vCont;c',
           'vCont?':'',
           'Hc0':'',
           'c':'',
           }

def Checksum(data):
    checksum = 0
    for c in data:
        checksum += ord(c)
    #return hex(checksum)[-2:]
    return checksum & 0xff

def ReadMemory(data):
    address = data[data.find('m')+1:data.find(',')]
    numBytes = data[data.find(',')+1:data.find('#')]
    print("Address:", address, "|| Number of bytes:", numBytes) # Debug information
    #send this to model and return answer value
    #THERE IS NO MODEL YET
    value = "2f86" #error code
    return value 

def ReadRegisters(data):
    #send this to model and return answer value
    #THERE IS NO MODEL YET
    #for example we take something from the model
    #for i in range(32):
    #    value+=registers[i]
    value = "123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0"
    return value

def WriteRegisters(data):
    registers = []
    for i in range(32):
        registers.append(data[1+8*i:9+i*8])
        #registers[i].send
    return "Ok"

def WriteRegisterN(data):
    register = data[data.find('P')+1:data.find('=')]
    value = data[data.find('=')+1:data.find('#')]
    #register.send-to-the-model
    return "Ok"

def WriteMemory(data):
    address = data[data.find('m')+1:data.find(',')]
    numBytes = data[data.find(',')+1:data.find(':')]
    value = data[data.find(':')+1:data.find('#')]
    #send this to model
    #THERE IS NO MODEL YET
    return "Ok"

def LastSignal(data):
    return "S00"

def Step():
    return LastSignal("+")

def Continue():
    return LastSignal("+")

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
            if (data.find(key) != -1):
                return switch[key]
    return 'Ok'

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
        ## getting 1kb of information from client,
        ## while client send it
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

        ## close socket
        print("Bye!")
        self.netout.close()
        self.clientsocket.close()
        log.close()
        conn.close()

#sock = socket.socket()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

## setting connection
port = int(input("Port = "))
sock.bind(('',port))
#sock.bind(('',3333)) ## связываем сокет с хостом и портом
sock.listen(1) ## max number of connections
conn, addr = sock.accept() ## getting a new socket and client's address
GDBClientHandler(conn).run()

#############################################################
#def qL12():   
