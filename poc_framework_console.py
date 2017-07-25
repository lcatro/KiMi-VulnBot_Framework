
import poc_framework_socket_pipe


'''
PoC FrameWork Dispatch Console :

  This Console can using to manager dispatch server by administrator and distributed interface ..

'''

if __name__ == '__main__' :  #  administrator console ..
    poc_framework_socket_pipe.pipe_console.init_pipe()
    poc_framework_socket_pipe.pipe_console.pipe_write('test_connect')

    welcome_string = poc_framework_socket_pipe.pipe_console.pipe_read()
    
    if not len(welcome_string) :
        print 'Connect to KiMi-VulnBot Dispatch Server Error ..'
        
    print welcome_string
    
    while True :
        command = raw_input('>').strip().lower()
        
        if 'quit'== command :
            print 'Console Exit ! '
            
            break
        else :
            poc_framework_socket_pipe.pipe_console.pipe_write(command)
            
            print poc_framework_socket_pipe.pipe_console.pipe_read()
            
else :  #  distributed interface ..
    print 'WARNING ! distributed interface will develepe ..'
