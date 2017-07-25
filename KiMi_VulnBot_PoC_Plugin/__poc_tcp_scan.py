
import random
import socket


def valid_vuln(host,port,other = None) :
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    result = False
    
    try :
        sock.settimeout(3)
        sock.connect((host,port))

        result = True
    except :
        pass
        
    sock.close()
        
    return result
    

if __name__ == '__main__' :  #  plugin debug
    print valid_vuln('127.0.0.1',80)
    print valid_vuln('127.0.0.1',135)
    print valid_vuln('127.0.0.1',3389)
    print valid_vuln('192.168.100.10',80)
    print valid_vuln('192.168.100.10',135)
    print valid_vuln('192.168.100.10',3389)
