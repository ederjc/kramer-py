import socket

IP_ADDR = '192.168.1.39'
TCP_PORT = 5000
BUFFER_SIZE = 1024

# This command changes protocol from 2000 to 3000 on machine 1
#s.send(b'\x38\x80\x83\x81')

class Kramer_switch():
    def __init__(self, ip_addr, tcp_port, machine_nr):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_addr = ip_addr
        self.tcp_port = tcp_port
        self.msg_prefix = str(machine_nr) + "@"
        self.SOCK_CON_TIMEOUT = 2.0
        self.SOCK_BUFFER_SIZE = 1024
        self.connected = False

    def connect(self):
        try:
            self.socket.connect((self.ip_addr, self.tcp_port))
            self.connected = True
        except Exception as e:
            print("Connection failed with excception: " + str(e))
            self.connected = False


    def close(self):
        self.socket.close()
        self.connected = False

    def communicate(self, payload):
        if not self.connected: self.connect()
        try:
            if payload == '':
                message = '#\r'
            else:
                message = '#' + str(payload) + '\r'
            self.socket.sendall(message.encode('ascii'))
        except Exception as e:
            print("Communication failed with excception: " + str(e))
            return False
        self.socket.settimeout(self.SOCK_CON_TIMEOUT)
        reply = self.socket.recv(self.SOCK_BUFFER_SIZE)
        return self.parseReply(reply)

    def parseReply(self, reply):
        reply = reply.decode('ascii')
        try:
            if reply[0] != '~' or reply[3] != '@':
                print('Invalid reply.')
                raise ValueError('Reply "' + (str(reply)) + '" invalid.')
            machine_number = int(reply[1:3])
            echo = ''
            for idx, char in enumerate(reply[4:]):
                if char == ' ' or char == '\r': break
                echo += char
            message = str(reply[idx+5:-2])
        except Exception as e:
            echo = ''
            message = ''
            machine_number = -1
            print("Error parsing reply: " + str(e))
        if 'ERR' in echo:
            try: error = int(echo[3:])
            except: error = -1
        else:
            error = ''
        return {
                'machine':machine_number,
                'echo':echo,
                'reply':message,
                'error_code':error
                }

    def checkConnection(self):
        if self.communicate('')['reply'] == 'OK': return 0
        else: return -1

    def getLoginLevel(self):
        return self.communicate('LOGIN?')

    def setLoginLevel(self, login_level, password):
        return self.communicate('LOGIN ' + str(login_level) + ',' + str(password))

    def getBuildDate(self):
        return self.communicate('BUILD-DATE?')

    def getModel(self):
        return self.communicate('MODEL?')

    def getProtocolVersion(self):
        return self.communicate('PROT-VER?')

    def setReset(self):
        return self.communicate('RESET')

    def getSerialNumber(self):
        return self.communicate('SN?')

    def getFwVersion(self):
        return self.communicate('VERSION?')

    def getOutputHpdStatus(self):
        return self.communicate('DISPLAY?')

    def getHwTemp(self):
        return self.communicate('HW-TEMP?')
    
    def getPresetList(self):
        return self.communicate('PRST-LST?')
          
    def getInputSignalStatus(self):
        return self.communicate('SIGNAL?')
   
    def setDhcpMode(self, dhcp_mode):
        '''
        Available DHCP modes:
        0 - Do not use DHCP
        1 - Try to use DHCP, if unavailable use static IP
        '''
        #return self.communicate('NET-DHCP ' + str(dhcp_mode))
        #return self.communicate('NET-DHCP?')

    def getMatrixStatus(self):
        return self.communicate('MATRIX-STATUS?')

    def getVideoSwitchState(self, out_port):
        return self.communicate('VID? ' + str(out_port))

    def setVideoSwitchState(self, in_port, out_port):
        return self.communicate('VID ' + str(in_port) + '>' + str(out_port))
