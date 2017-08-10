# -- coding: cp1251 --
#! /usr/bin/python3
import socket

#import local modules
import helper

def Checksum(data):
    checksum = 0
    for c in data:
        checksum += ord(c)
    #return hex(checksum)[-2:]
    return checksum & 0xff

def parse(data):
    if data.startswith('$'):
        data = '$' + data.split('$')[-1]
    return data

class GDBClientHandler(object):
    def __init__(self, clientsocket):
        self.clientsocket = clientsocket
        self.netin = clientsocket.makefile('r')
        self.netout = clientsocket.makefile('w')
        #self.last_pkt = None

    def send(self, msg):
        self.send_raw('+$%s#%.2x' % (msg, Checksum(msg)))
    def send_raw(self, r):
        self.netout.write(r)
        self.netout.flush()

    def TestMessage(self):
        #msg="oSomeday this server will be fully working but not now!"
        msg=b'Hello'
        msg='O'+msg
        cs=Checksum(msg)
        try:
            self.send(msg)
            print("Sending: ", msg)
        except Exception:
            print("Client is not answering.")

    def InteruptMessage(self):
        try:
            self.netout = clientsocket.makefile('wb')
            self.send_raw('\003')
            print("Sending: ", msg)
            self.netout = clientsocket.makefile('w')
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
                #self.TestMessage()
                print("there's nothing to answer!")
                continue
            else:
                msg=helper.Message(data)
                pastMsg = msg
            cs=Checksum(msg)
            #try:
            #    self.send(msg)
            #    print("Sending: ", msg)
            #except Exception:
            #    print("Client is not answering.")
            if (msg == "interrupt"):
                self.InteruptMessage()
                print("Sending: ", msg)
            else:
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
            
            if ((data == '$D#44') or (data == '\003')):
                break

        ## close socket
        print("Bye!")
        ##self.TestMessage()
        self.netout.close()
        self.clientsocket.close()
        log.close()
        conn.close()

#if __name__ == "__main__":
#    data = '$m1700,2#12'
#    msg=helper.Message(data)
#    print(msg)


#sock = socket.socket()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

## setting connection
port = int(input("Port = "))
sock.bind(('',port))
#sock.bind(('',3333)) ##
sock.listen(1) ## max number of connections
conn, addr = sock.accept() ## getting a new socket and client's address
GDBClientHandler(conn).run()
