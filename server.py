# -- coding: cp1251 --
import socket

switch = { #'$qSupported':'swbreak+;PacketSize=131072', #119?   131072
           '$qSupported':'PacketSize=131072',
           #'$vMustReplyEmpty':'',
           '$Hg0':'OK',
           '$Hg-1':'OK',
           '$qTStatus':'',
           #'+$S':'T05',
           '$qfThreadInfo':'m0',
           '$qsThreadInfo':'l',
           '$Hc-1':'OK',
           '$qC':'',
           '$qAttached':'1',
           '$qOffsets':'Text=00;Data=00;Bss=0',
            '$g#67':'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 
           '$p20':'0010000000000000',
           '$qSymbol':'',
           '$vKill':'OK',
           '+$?':'S00',
           '$qTfV':'',
           '$qTsP':'',
           #'$qL12':'',
           '$qL12':'0x0000000000001000 in ?? ()',
           #'vCont?':'vCont;c',
           #'vCont?':'',
           'Hc0':'',
           'c':'',
           '$#':'',
           '$D':'OK'
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
    value = "0000803f" #error code
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
    return "OK"

def WriteMemory(data):
    address = data[data.find('m')+1:data.find(',')]
    numBytes = data[data.find(',')+1:data.find(':')]
    value = data[data.find(':')+1:data.find('#')]
    #send this to model
    #THERE IS NO MODEL YET
    return "OK"

def LastSignal(data):
    return "S00"

def Step():
    #return LastSignal("+")
    return 'T05'

def Continue():
    return LastSignal("+")

def SetMemory(data):
    address = data[data.find('X')+1:data.find(',')]
    length = data[data.find(',')+1:data.find(':')]
    value = data[data.find(':')+1:data.find('#')]
    #send this to model
    #THERE IS NO MODEL YET
    return "OK"

def InsertBreakpoint(data):
    ztype = data[data.find('Z')+1:data.find(',')]
    temp = data[data.find(',')+1:]
    address = temp[:temp.find(',')]
    value = temp[temp.find(',')+1:data.find('#')]
    #send this to model
    #THERE IS NO MODEL YET
    return "OK"

def DeleteBreakpoint(data):
    ztype = data[data.find('Z')+1:data.find(',')]
    temp = data[data.find(',')+1:]
    address = temp[:temp.find(',')]
    value = temp[temp.find(',')+1:data.find('#')]
    #send this to model
    #THERE IS NO MODEL YET
    return "OK"

def VQuery(data):
    if (data.find('$vCont?') != -1):
        return 'vCont;c;s;t;r start,end'
    if (data.find('$vCont;s') != -1):
        return 'vCont;c;s;t;r start,end'
        
    if (data.find('$vCtrlC') != -1):
        printf("Client interrupt the process")
    if (data.find('$vKill') != -1):
        printf("Client kill the process")
    if (data.find('$vStopped') != -1):
        printf("Client stopped the process")
    if (data.find('$vMustReplyEmpty') != -1):
        return ''
    return "OK"

def Message(data):
    print('Data: ', data)
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
    elif (data.find('$X') != -1):
        return SetMemory(data)
    elif (data.find('$Z') != -1):
        return InsertBreakpoint(data)
    elif (data.find('$z') != -1):
        return DeleteBreakpoint(data)
    elif (data.find('$v') != -1):
        return VQuery(data)
    else:
        for key in switch:
            if (data.find(key) != -1):
                return switch[key]
    return 'OK'

def parse(data):
    if data.startswith('$'):
        data = '$' + data.split('$')[-1]
    return data

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

    def TestMessage(self):
        #msg="OSomeday this server will be fully working but not now!"
        msg='o48656c6c6f2c20776f726c64210a'
        cs=Checksum(msg)
        try:
            self.send(msg)
            print("Sending: ", msg)
        except Exception:
            print("Client is not answering.")
   
    def run(self):
        print("connected:", addr)
        log = open("log.txt", 'w')
        msg, cs = "",""
        data = ''
        pastData = ''
        pastMsg = ''
        ## getting 1kb of information from client,
        ## while client send it
        while True:
            pastData=data
            while (data==pastData):
                data = str(conn.recv(1024).decode('cp1251'))
            log.write(data)
            log.write("\n")
            print("Received: ", data)
            data=parse(data)
            if (data=='+'):
                #msg = pastMsg
                print("there's nothing to answer!")
                continue
            else:
                msg=Message(data)
                pastMsg = msg
            cs=Checksum(msg)
            try:
                self.send(msg)
                print("Sending: ", msg)
            except Exception:
                print("Client is not answering.")

            ## one time JOKE
            #if (data=='+$qSymbol::#5b'):
            #    self.TestMessage()

            log.write("+$"+str(msg)+"#"+str(cs)[-2:])
            log.write("\n")
            
            if (data == '$D#44'):
                break

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
