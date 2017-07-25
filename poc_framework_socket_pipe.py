
import socket


class local_loop_address :
    
    ipv4 = '127.0.0.1'

class pipe_dispatch :
    
    pipe_dispatch_port = 10010
    __pipe_dispatch_socket = None
    __pipe_receive_buffer_length = 4096
    
    @staticmethod
    def init_pipe() :
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        
        sock.setblocking(True)
        sock.bind((local_loop_address.ipv4,pipe_dispatch.pipe_dispatch_port))
        
        pipe_dispatch.__pipe_dispatch_socket = sock

    @staticmethod
    def pipe_write(data) :
        pipe_dispatch.__pipe_dispatch_socket.sendto(data,(local_loop_address.ipv4,pipe_console.pipe_console_port))
        
    @staticmethod
    def pipe_read() :
        data,address = pipe_dispatch.__pipe_dispatch_socket.recvfrom(pipe_dispatch.__pipe_receive_buffer_length)
        
        if local_loop_address.ipv4 == address[0] :
            return data
        
        return None

class pipe_console :
    
    pipe_console_port = pipe_dispatch.pipe_dispatch_port + 1
    __pipe_console_socket = None
    __pipe_receive_buffer_length = 4096
    
    @staticmethod
    def init_pipe() :
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        
        sock.setblocking(True)
        sock.bind((local_loop_address.ipv4,pipe_console.pipe_console_port))
        
        pipe_console.__pipe_console_socket = sock

    @staticmethod
    def pipe_write(data) :
        pipe_console.__pipe_console_socket.sendto(data,(local_loop_address.ipv4,pipe_dispatch.pipe_dispatch_port))
        
    @staticmethod
    def pipe_read() :
        data,address = pipe_console.__pipe_console_socket.recvfrom(pipe_console.__pipe_receive_buffer_length)
        
        if local_loop_address.ipv4 == address[0] :
            return data
        
        return None


if __name__ == '__main__' :  #  test case ..
    pipe_dispatch.init_pipe()
    pipe_console.init_pipe()
    pipe_dispatch.pipe_write('AAAAAA')
    
    print pipe_console.pipe_read()
