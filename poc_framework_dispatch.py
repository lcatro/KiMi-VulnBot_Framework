
import local_system
import poc_framework_report_queue
import poc_framework_scan_plugin
import poc_framework_socket_pipe


class task :
    
    def __init__(self,scan_plugin_name,scan_host_session,scan_port_session = [80],max_thread_count = 600) :
        self.max_thread_count = max_thread_count
        self.current_running_thread = 0
        self.thread_lock = local_system.thread_lock()
        self.update_lock = local_system.thread_lock()
        self.queue_lock = local_system.thread_lock()
        self.scan_plugin_name = scan_plugin_name
        self.scan_process = 0
        self.scan_host_session = scan_host_session
        self.scan_port_session = scan_port_session
        self.host_session_length = len(self.scan_host_session)
        self.port_session_length = len(self.scan_port_session)
        self.task_loop = True
        self.wait_for_exit = True
        
        if 0 == self.port_session_length :
            self.port_session_length = 1
        
        self.task_count = self.host_session_length * self.port_session_length
        
        if not poc_framework_scan_plugin.is_exist_plugin(scan_plugin_name) :
            raise ValueError,'WARNING ! Can\'t Found the Scan Plugin :' + scan_plugin_name
        
    def get_task_name(self) :
        return self.scan_plugin_name
        
    def get_task_scan_process(self) :
        return self.scan_process
        
    def __set_task_scan_process(self,process) :
        self.scan_process = process
        
    def get_current_running_thread(self) :
        self.thread_lock.enter_lock()
        
        result = self.current_running_thread
        
        self.thread_lock.exit_lock()
        
        return result
        
    def __add_a_running_thread(self) :
        self.thread_lock.enter_lock()
        
        self.current_running_thread += 1
        
        self.thread_lock.exit_lock()
        
    def __remove_a_running_thread(self) :
        self.thread_lock.enter_lock()
        
        self.current_running_thread -= 1
        
        if self.queue_lock.is_lock() :
            self.queue_lock.exit_lock()  #  TIPS : exit queue lock at this will promoting a little performance .
                                         #  look code at self.queue_lock.lock() and self.get_current_running_thread()
                                         #  in __internal_task_execute_queue ..
        self.thread_lock.exit_lock()
        
    @staticmethod
    def __internal_task_thread(thread_argument_list) :
        self = thread_argument_list[0]
        vuln_name = thread_argument_list[1]
        target_host = thread_argument_list[2]
        target_port = thread_argument_list[3]
        
#        print target_host,target_port
        
        self.__add_a_running_thread()
        
        #  WARNING ! There are not try-catch for capture plugin excute exception
        if not None == target_port :
            result = poc_framework_scan_plugin.call_plugin(self.scan_plugin_name,target_host,target_port)
        else :
            result = poc_framework_scan_plugin.call_plugin(self.scan_plugin_name,target_host)
        
        if result :
            self.update_lock.enter_lock()
            
#            site_count = poc_framework_report_queue.poc_report_cache.get_report_site_data(vuln_name) + 1
            print 'Live:',target_host,target_port
#            poc_framework_report_queue.poc_report_cache.set_report_site_data(vuln_name,site_count)
            
            self.update_lock.exit_lock()
        
        self.__remove_a_running_thread()
        
    @staticmethod
    def __internal_task_execute_queue(thread_argument_list) :
#        print 'Enter __internal_task_execute_queue'
        
        executed_task_index = 0
        self = thread_argument_list[0]
        
        while self.task_loop and executed_task_index < self.task_count :
            create_new_task_thread_count = self.max_thread_count - self.get_current_running_thread()
            
            if create_new_task_thread_count :
                for create_new_task_thread_index in range(create_new_task_thread_count) :
                    target_host_index = executed_task_index / self.port_session_length
                    target_port_index = executed_task_index % self.port_session_length
                    
#                    print 'Dispatch Task Index ,host:',self.scan_host_session[target_host_index], \
#                                               'port:',self.scan_port_session[target_port_index]
                    
                    local_system.create_thread(task.__internal_task_thread,
                                               (self,
                                                self.scan_plugin_name,
                                                self.scan_host_session[target_host_index],
                                                self.scan_port_session[target_port_index]
                                               ),
                                               True)  #  all sub-thread is daemon thread ,they will exit follow return
                    
                    executed_task_index += 1
                    
                    self.__set_task_scan_process(executed_task_index / float(self.task_count))
                    
                    if executed_task_index >= self.task_count :  #  all task executed ..
                        return
                    
                if self.get_current_running_thread() < self.max_thread_count :
                    continue
                    
                if self.queue_lock.is_lock() :
                    try :
                        self.queue_lock.exit_lock()  #  TIPS : clear lock
                    except :
                        pass
                    
                self.queue_lock.enter_lock()  #  TIPS : pre-enter deadlock
            
            self.queue_lock.enter_lock()  #  TIPS : wait for __remove_a_running_thread unlock until __internal_task_thread exit
            
        if self.wait_for_exit :  #  WARNING ! __internal_task_execute_queue() create daemon thread ,
                                 #  all thread will exit when __internal_task_execute_queue() return 
#            print 'Wait For All Threads Exit ..'
                
            while self.get_current_running_thread() :
                self.queue_lock.lock(1)   #  TIPS : enter lock for check running thread list ..
                
#        print 'Exit __internal_task_execute_queue'
            
    def run(self) :
        self.task_loop = True
        self.wait_for_exit = True
        self.scan_process = 0
        
        local_system.create_thread(task.__internal_task_execute_queue,(self,))
    
    def exit(self) :
        self.wait_for_exit = True
        self.task_loop = False

    def force_exit(self) :
        self.wait_for_exit = False
        self.task_loop = False
        

def command_resolver(command) :
    command_argument_list = command.split(' ')
    
    if len(command_argument_list) :
        if 1 == len(command_argument_list) :
            return command_argument_list[0] , []
        else :
            return command_argument_list[0] , command_argument_list[1:]
    
    return '', []


if __name__ == '__main__' :
    print 'Init Dispatch Server'
    
    poc_framework_socket_pipe.pipe_dispatch.init_pipe()
    poc_framework_report_queue.poc_report_update_queue.run_dispatch()

    print 'Enter Server'
    
    scan_task_list = []
    
    while True :
        command,command_arguments = command_resolver(poc_framework_socket_pipe.pipe_dispatch.pipe_read())
        
        print 'Receive Command :',command,command_arguments
        
        if len(command) :
            if 'test_connect' == command :
                poc_framework_socket_pipe.pipe_dispatch.pipe_write('There is KiMi-Bot Scan Task Dispatch Server ...')
                
            elif 'create' == command :  #  command format 1 :
                                        #  create %vuln_name% network %network_segment% %network_mask% [%port%] (%thread%))
                                        #  %port% ===list format==> [port1,port2,lower_bound-upper_bound]
                                        #  command format 2 :
                                        #  create %vuln_name% host 
                                        #  > host 1  #  input scan host list
                                        #  > host 2
                                        #  > ...
                                        #  > port_list  #  conver to input scan port list
                                        #  > 80
                                        #  > 8080
                                        #  > 10086
                                        #  > submit_task  #  submit task for execute
                                        #  command format 3 :
                                        #  create %vuln_name% url 
                                        #  > url 1  #  input scan host list
                                        #  > url 2
                                        #  > url 3
                                        #  > ...
                                        #  > submit_task  #  submit task for execute
                                        #  
                vuln_name = command_arguments[0]
                command_format = command_arguments[1]
                
                print 'Create Task :',vuln_name,command_format
                
                if not poc_framework_scan_plugin.is_exist_plugin(vuln_name) :
                    print vuln_name,'is invalid Plugin ..'
                    
                    continue
                
                if 'network' == command_format :
                    network_segment = local_system.ip_address_to_number(command_arguments[2])  #  WARNING ! big-endian
                    network_segment = local_system.big_endian_number_conver(network_segment)
                    network_mask = int(command_arguments[3])  #  24
                    network_ip_count = pow(2,32 - network_mask)
                    network_last_ip = network_segment + network_ip_count
                    network_ip_list = []
                    
                    print 'Network Session [',local_system.number_to_ip_address(network_segment), \
                                              local_system.number_to_ip_address(network_last_ip), \
                                              ']',str(network_ip_count)
                    
                    for network_index in range(network_ip_count) :
                        network_ip_index = local_system.big_endian_number_conver(network_segment + network_index)
                        
                        network_ip_list.append(local_system.number_to_ip_address(network_ip_index))
                    
                    if 5 <= len(command_arguments) :
                        port_list_ = command_arguments[4]
                        port_list_ = port_list_.replace('[','')
                        port_list_ = port_list_.replace(']','')
                        port_list_ = port_list_.split(',')
                        port_list  = []
                        
                        if not '*' == port_list_[0] :  #  [*]
                            for port_index in port_list_ :
                                if '-' in port_index :
                                    lower_bound = port_index.split('-')
                                    upper_bound = lower_bound[1]
                                    lower_bound = lower_bound[0]

                                    if lower_bound < upper_bound :
                                        for index in range(upper_bound - lower_bound) :
                                            port_list.append(lower_bound + port_index)
                                    else :  #  error ..
                                        pass
                                else :
                                    port_list.append(int(port_index))
                        else :
                            for port_index in range(65532) :
                                port_list.append(port_index)
                                        
#                        print 'Port List:',port_list
                        print 'Ready to Run Plugin ..'
                    
                        scan_task = task(vuln_name,network_ip_list,port_list)
                    else :
                        print 'Ready to Run Plugin ..'
                        
                        scan_task = task(vuln_name,network_ip_list)
                        
                    scan_task_list.append(scan_task)
                    scan_task.run()
                        
                elif 'host' == command_format :
                    pass  #  hahahahaha ..
                
                
            
                poc_framework_socket_pipe.pipe_dispatch.pipe_write('Task is Running ..')
            elif 'delete' == command :  #  delete %vuln_name%
                for scan_task_index in len(scan_task_list) :
                    scan_task_index_object = scan_task_list[scan_task_index]
                    
                    if not scan_task_index_object.get_task_name() == command_arguments[0] :
                        continue
                        
                    if scan_task_index_object.get_current_running_thread() :
                        poc_framework_socket_pipe.pipe_dispatch.pipe_write('Task has ' + \
                                                                           str(scan_task_index_object.get_current_running_thread()) + \
                                                                           ' Running ,Do You want exit ? [yes|force|no]:'
                                                                          )

                        command = poc_framework_socket_pipe.pipe_dispatch.pipe_read()

                        if len(command) :
                            if command.startswith('yes') :
                                scan_task_index_object.exit()
                                scan_task_list.pop(scan_task_index)
                            elif command.startswith('force') :
                                scan_task_index_object.force_exit()
                                scan_task_list.pop(scan_task_index)

                        break
                                
                poc_framework_socket_pipe.pipe_dispatch.pipe_write('Delete Task ..')
                
            elif 'queue' == command :
                for scan_task_index in scan_task_list :
                    output = scan_task_index.get_task_name() + '(' + \
                           + 'RunningThread:' + \
                           + str(get_current_running_thread) + ',' + \
                           + 'Progress:' + \
                           + str(scan_task_index.get_task_scan_process()) + ')\n'
                
                    poc_framework_socket_pipe.pipe_dispatch.pipe_write(output)
                    
            elif 'quit' == command :
                break
        else :
            poc_framework_socket_pipe.pipe_dispatch.pipe_write('Oops ,nothing ...')
    
    print 'KiMi-Bot Dispatch Server Exited'
else :
    print 'You need Running by Python instead of Import ..'
