
import sys

import local_system


poc_plugin_directory = 'KiMi_VulnBot_PoC_Plugin'
poc_plugin_entry_function_name = 'valid_vuln'
poc_plugin_prefix_name = '__poc_'
poc_plugin_python_extension_name = '.py'

sys.path.append(poc_plugin_directory)  #  load_plugin_directory


def get_plugin() :
    files = local_system.get_directory_files(local_system.get_current_path() + poc_plugin_directory)
    poc_plugin_list = []
    
    for file_index in files :
        if file_index.startswith(poc_plugin_prefix_name) and file_index.endswith(poc_plugin_python_extension_name) :
            poc_plugin_name = file_index[file_index.find(poc_plugin_prefix_name) + len(poc_plugin_prefix_name) : \
                                         file_index.rfind(poc_plugin_python_extension_name)]
            
            poc_plugin_list.append(poc_plugin_name)

    if len(poc_plugin_list) :
        return poc_plugin_list

    return None

def is_exist_plugin(plugin_name) :
    poc_plugin_file_path  = local_system.get_current_path() + poc_plugin_directory + local_system.get_system_directory_separator()
    poc_plugin_file_path += poc_plugin_prefix_name + plugin_name + poc_plugin_python_extension_name
    
    return local_system.is_exist_file(poc_plugin_file_path)

def call_plugin(plugin_name,host,port = 80,other = {}) :
    plugin_name = poc_plugin_prefix_name + plugin_name
    
    exec('import ' + plugin_name)
    exec('plugin_function_list = dir(' + plugin_name + ')')  #  TIPS : plugin_name is string ,dir() need a module object

    if not poc_plugin_entry_function_name in plugin_function_list :
        raise ValueError,'Load PoC Plugin Error ,Can\'t Found Plugin Entry Function ..'

    result_value = False
        
    try :
        exec('result_value = ' + plugin_name + '.' + poc_plugin_entry_function_name + '(host,port,other)')
    except Exception,e :  #  WARNING ! collect plugin exception instead of that crash the scan framework ..
        raise Warning,'Running Plugin valid_vuln() Error ..\n' + e.message
        
#    exec('del ' + plugin_name)  #  TIPS : import python library will free after return by function

    return result_value


if __name__ == '__main__' :  #  test case ..
    '''
    test_plugin_name = 'test'
    
    print get_plugin()

    start_time = local_system.get_timetick()
    
    for index in range(10000) :
        call_plugin(test_plugin_name,'')
    
    print 'Using Time :' + str(local_system.get_timetick() - start_time)  #  0.417999 s
    '''
