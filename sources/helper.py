# -- coding: cp1251 --
#! /usr/bin/python3
import config

# variables for tests
import var
m_value = var.memory
r_value = var.registers
ls_value = var.lastSignal
s_value = var.step
c_value = var.cont
pc_value = var.pc

# Functions proceeding information

def Output(data):
    # data is decimal value
    value = hex(data)[2:]
    if (len(value) % 2) == 1:
        value = '0' + value
    word = ''
    for i in range(len(value) // 2):
        word += value[-2:]
        value = value[:-2]
    # int(a,16) -> convert to decimal
    return word

def ReadMemory(data):
    address = data[data.find('m')+1:data.find(',')]
    numBytes = data[data.find(',')+1:data.find('#')]
    print("Address:", address, "|| Number of bytes:", numBytes) # Debug information
    #send this to model and return answer value
    #THERE IS NO MODEL YET 
    return Output(m_value) 

def ReadRegisters(data):
    #send this to model and return answer value
    #THERE IS NO MODEL YET
    #for example we take something from the model
    #for i in range(32):
    #    value+=registers[i]
    return r_value

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
    return ls_value

def Step(data):
    #return LastSignal("+")
    #return 'T05'
    return s_value

def Continue(data):
    #return LastSignal("+")
    return c_value

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
    if (data.find('$vCont;c') != -1):
        return 'T0501:7ffff850;40:3000ce98'    
    if (data.find('$vCont?') != -1):
    #    return 'vCont;c;C;s;S'
        return ""
    #if ((data.find('$vCont') != -1) and ((data.find('s') != -1) or (data.find('c') != -1) or (data.find('t') != -1))):
    #    return 'vCont;c;s;t'

    if (data.find('$vCtrlC') != -1):
        printf("Client interrupt the process")
    if (data.find('$vKill') != -1):
        printf("Client kill the process")
    if (data.find('$vStopped') != -1):
        printf("Client stopped the process")
    if (data.find('$vMustReplyEmpty') != -1):
        return ''
    return "OK"

def PCQuery(data):
    #
    return Output(pc_value)

mSwitch={
    '$m':ReadMemory,
    '$g':ReadRegisters,
    '$G':WriteRegisters,
    '$P':WriteRegisterN,
    '$M':WriteMemory,
    '$?':LastSignal,
    '$s':Step,
    '$c':Continue,
    '$X':SetMemory,
    '$Z':InsertBreakpoint,
    '$z':DeleteBreakpoint,
    '$v':VQuery,
    '$p20':PCQuery,
    }

def Message(data):
    print('Data: ', data)
    for key in mSwitch:
        if (data.find(key) != -1):
            return mSwitch[key](data)
    else:
        for key in config.switch:
            if (data.find(key) != -1):
                return config.switch[key]
    return 'OK'
