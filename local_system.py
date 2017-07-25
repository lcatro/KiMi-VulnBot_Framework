
import os
import platform
import socket
import sys
import thread
import threading
import time


def debug_print(debug_string) :
    print debug_string
    
def debug_var_dump(debug_object) :
    print debug_object

def get_timetick() :
    return time.time()

def get_system() :
    system = platform.system()
    
    if 'Windows' == system :
        return 1
    if 'Linux' == system :
        return 2
    if 'MacOS' == system :
        return 3
    
    return 0
    
def get_system_directory_separator() :
    if 1 == get_system() :
        return '\\'
    
    return '/'
    
def get_current_path() :
    offset = sys.argv[0].rfind(get_system_directory_separator())
        
    current_file_path = sys.argv[0][ : offset + 1]
    
    return current_file_path
    
def get_directory_files(directory_path) :
    return os.listdir(directory_path)
    
def is_exist_directory(path) :
    return os.path.isdir(path)
    
def is_exist_file(path) :
    return os.path.isfile(path)
    
def create_directory(path) :
    return os.mkdir(path)
    
def copy_file(source_file_path,destination_file_path) :
    source_file_data = read_file(source_file_path)
    
    write_file(destination_file_path,source_file_data)
    
def copy_directory(source_path,destination_path) :
    directory_char = get_system_directory_separator()
    
    if not is_exist_directory(destination_path) :
        os.mkdir(destination_path)
            
    for walk_index in os.walk(source_path) :
        walk_source_path = walk_index[0]
        
        first_directory_offset = walk_source_path.find(directory_char)

        if not -1 == first_directory_offset :
            copy_target_directory = destination_path + directory_char + walk_index[0][first_directory_offset + 1:]
        else :
            copy_target_directory = destination_path + directory_char
        
        if not is_exist_directory(copy_target_directory) :
            os.mkdir(copy_target_directory)
        
        for file_index in walk_index[2] :
            copy_file(walk_index[0] + directory_char + file_index,copy_target_directory + directory_char + file_index)

def read_file(file_path) :
    file = open(file_path,'r')
    result = ''
    
    if file :
        result = file.read()
        
    file.close()
    
    return result
    
def write_file(file_path,data) :
    file = open(file_path,'w')
    
    if file :
        file.write(data)
        
    file.close()
    
def sleep(sleep_time) :
    time.sleep(sleep_time)
    
def ip_address_to_number(ip_address) :
    address_number = socket.inet_aton(ip_address)
    
    return_number  = ord(address_number[0])
    return_number += ord(address_number[1]) * 0x100
    return_number += ord(address_number[2]) * 0x10000
    return_number += ord(address_number[3]) * 0x1000000

    return return_number
    
def number_to_ip_address(number) :
    address_byte = ''
    
    address_byte += str((number & 0xFF)) + '.'
    address_byte += str((number & 0xFFFF) / 0x100) + '.'
    address_byte += str((number & 0xFFFFFF) / 0x10000) + '.'
    address_byte += str((number & 0xFFFFFFFF) / 0x1000000)
    
    return address_byte
    
def big_endian_number_conver(number) :
    result = 0
    
    result += (number & 0xFF000000) / 0x1000000
    result += (number & 0xFF0000) / 0x100
    result += (number & 0xFF00) * 0x100
    result += (number & 0xFF) * 0x1000000
    
    return result
    
def create_thread(thread_function,thread_arguments = (),is_sub_thread = False) :
#    thread.start_new_thread(thread_function,thread_arguments)
    thread = thread_object(thread_function,thread_arguments,is_sub_thread)
    
    thread.start()
    
    return thread

class thread_object(threading.Thread) :
    
    def __init__(self,thread_function,thread_arguments = (),is_sub_thread = False) :
        threading.Thread.__init__(self)
        
        self.thread_function = thread_function
        self.thread_arguments = thread_arguments
        
        if is_sub_thread :
            self.setDaemon(True)
        
    def run(self) :
        if len(self.thread_arguments) :
            self.thread_function(self.thread_arguments)
        else :
            self.thread_function()
            
    def exit(self) :
        self._Thread__stop()
        
class thread_lock :
    
    def __init__(self) :
        self.thread_lock = thread.allocate_lock()
    
    def enter_lock(self,timeout = 0) :
        if timeout :
            self.thread_lock.acquire(timeout)
        else :
            self.thread_lock.acquire()
    
    def exit_lock(self) :
        self.thread_lock.release()
        
    def is_lock(self) :
        return self.thread_lock.locked()
    
    
if __name__ == '__main__' :  # test case ..
#    copy_directory('report_templete','test')
    
    ip = '127.0.0.1'
    
    print ip_address_to_number(ip)
    print big_endian_number_conver(ip_address_to_number(ip))
    print number_to_ip_address(big_endian_number_conver(ip_address_to_number(ip)))
    print big_endian_number_conver(big_endian_number_conver(ip_address_to_number(ip)))
    print number_to_ip_address(big_endian_number_conver(big_endian_number_conver(ip_address_to_number(ip))))
    