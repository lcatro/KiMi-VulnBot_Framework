
import json

import github_api
import local_system


'''
KiMi-VulnBot github auth-key :
'''

github_organization_name = 'KiMiThreatPerception'
github_user_name = 'KiMi-VulnBot'
github_authorization_key = ''

'''
PoC Report Cache  --  Save Current Report Cache
'''

class poc_report_cache :
    
    __inside_cache = {
        
    }
    __thread_lock = local_system.thread_lock()
    
    @staticmethod
    def get_report_site_data(report_name,city_name) :
        return_data = None
        
        poc_report_cache.__thread_lock.enter_lock()
        
        if poc_report_cache.__inside_cache.has_key(report_name) :
            if poc_report_cache.__inside_cache.has_key[report_name]['site_data'].has_key(report_name) :
                return_data = poc_report_cache.__inside_cache[report_name]['site_data'][city_name]
            
        poc_report_cache.__thread_lock.exit_lock()
            
        return return_data
    
    @staticmethod
    def get_report_analysis_report(report_name) :
        return_data = None
        
        poc_report_cache.__thread_lock.enter_lock()
        
        if poc_report_cache.__inside_cache.has_key(report_name) :
            return_data = poc_report_cache.__inside_cache[report_name]['analysis_report']
            
        poc_report_cache.__thread_lock.exit_lock()
            
        return return_data
    
    @staticmethod
    def set_report_site_data(report_name,city_name,vuln_host_number) :
        poc_report_cache.__thread_lock.enter_lock()
        
        if poc_report_cache.__inside_cache.has_key(report_name) :
            poc_report_cache.__inside_cache[report_name]['site_data'][city_name] = vuln_host_number
            
        poc_report_cache.__thread_lock.exit_lock()
    
    @staticmethod
    def set_report_analysis_report(report_name,analysis_report_data) :
        poc_report_cache.__thread_lock.enter_lock()
        
        if poc_report_cache.__inside_cache.has_key(report_name) :
            poc_report_cache.__inside_cache[report_name]['analysis_report'] = analysis_report_data
            
        poc_report_cache.__thread_lock.exit_lock()

    @staticmethod
    def clear_report_site_data(report_name) :
        poc_report_cache.__thread_lock.enter_lock()
        
        if poc_report_cache.__inside_cache.has_key(report_name) :
            poc_report_cache.__inside_cache[report_name]['site_data'] = {}
            
        poc_report_cache.__thread_lock.exit_lock()
    
    @staticmethod
    def clear_analysis_report(report_name) :
        poc_report_cache.__thread_lock.enter_lock()
        
        if poc_report_cache.__inside_cache.has_key(report_name) :
            poc_report_cache.__inside_cache[report_name]['analysis_report'] = {}
            
        poc_report_cache.__thread_lock.exit_lock()
    
    @staticmethod
    def is_exist_report(report_name) :
        poc_report_cache.__thread_lock.enter_lock()
        
        result = poc_report_cache.__inside_cache.has_key(report_name)
        
        poc_report_cache.__thread_lock.exit_lock()
        
        return result
        
    @staticmethod
    def add_report(report_name) :
        poc_report_cache.__thread_lock.enter_lock()
        
        poc_report_cache.__inside_cache[report_name] = {}
        poc_report_cache.__inside_cache[report_name]['site_data'] = site_data
        poc_report_cache.__inside_cache[report_name]['analysis_report'] = analysis_report_data
            
        poc_report_cache.__thread_lock.exit_lock()
        
'''
PoC Report Operate API  --  Github API
'''

class poc_operate_api :
    
    __poc_report_root_directory = github_organization_name + '.github.io' + local_system.get_system_directory_separator() \
                                + 'vuln_report_data' + local_system.get_system_directory_separator()

    @staticmethod
    def is_exist_report(vuln_report_name) :
        return local_system.is_exist_directory(poc_operate_api.__poc_report_root_directory + vuln_report_name)

    '''
    @staticmethod
    def load_report(vuln_report_name) :
        if poc_operate_api.is_exist_report(vuln_report_name) :
            report_dir = poc_operate_api.__poc_report_root_directory + vuln_report_name + local_system.get_system_directory_separator()
            site_data_json_file = report_dir + 'site_data.json'
            analysis_report_json_file = report_dir + 'analysis_report.json'

            if local_system.is_exist_file(site_data_json_file) and local_system.is_exist_file(analysis_report_json_file) :
                site_data_file_content = local_system.read_file(site_data_json_file)
                analysis_report_file_content = local_system.read_file(analysis_report_json_file)

                site_data_file_content_json = json.loads(site_data_file_content)
                analysis_report_file_content_json = json.loads(analysis_report_file_content)

                poc_report_cache.add_report(vuln_report_name,site_data_file_content_json,analysis_report_file_content_json)

                return True

        return False
    '''

    @staticmethod
    def create_report(vuln_report_name) :
        if not poc_operate_api.is_exist_report(vuln_report_name) :
            report_dir = poc_operate_api.__poc_report_root_directory + vuln_report_name + local_system.get_system_directory_separator()
            
            local_system.create_directory(report_dir)
            
            site_data_json_file = report_dir + 'site_data.json'
            analysis_report_json_file = report_dir + 'analysis_report.json'
            
            local_system.write_file(site_data_json_file,json.dumps({}))
            local_system.write_file(analysis_report_json_file,json.dumps({}))
            
            poc_report_cache.add_report(vuln_report_name)
                
            return True
        
        return False
    
    @staticmethod
    def upload_report(vuln_report_name) :
        if poc_operate_api.is_exist_report(vuln_report_name) :
#            local_system.debug_print(vuln_report_name)

            update_report(vuln_report_name)  #  WARNING ! git pull before git push .
                                             #  try git push it will make git error that remote repository is lastly but local is not lastly ..
                                             
            report_dir = poc_operate_api.__poc_report_root_directory + vuln_report_name + local_system.get_system_directory_separator()
            site_data_json_file = report_dir + 'site_data.json'
            analysis_report_json_file = report_dir + 'analysis_report.json'
            
            updated_site_data = json.loads(local_system.read_file(site_data_json_file))
            updated_analysis_report = json.loads(local_system.read_file(analysis_report_json_file))
            
            temporary_scan_data_list = poc_report_cache.get_report_site_data(vuln_report_name)
            
            if not None == temporary_scan_data_list :
                for temporary_scan_data_index in temporary_scan_data_list :
                    temporary_value = temporary_scan_data_list[temporary_scan_data_index]

                    if updated_site_data.has_key(temporary_scan_data_index) :
                        updated_site_data[temporary_scan_data_index] += temporary_value
                    else :
                        updated_site_data[temporary_scan_data_index]  = temporary_value
                        
                local_system.write_file(site_data_json_file,json_dumps(updated_site_data))
                    
            temporary_analysis_data_list = poc_report_cache.get_report_analysis_report(vuln_report_name)
            
            if not None == temporary_analysis_data_list :
                for temporary_analysis_data_index in temporary_analysis_data_list :
                    temporary_value = temporary_scan_data_list[temporary_analysis_data_index]

                    if updated_analysis_report.has_key(temporary_analysis_data_index) :
                        updated_analysis_report[temporary_analysis_data_index] += temporary_value
                    else :
                        updated_analysis_report[temporary_analysis_data_index]  = temporary_value

                local_system.write_file(analysis_report_json_file,json_dumps(updated_analysis_report))
            
            if not None == temporary_scan_data_list or not None == temporary_scan_data_list :
                github_api.report_tool_kit.upload_report(github_organization_name + '.github.io')
            
                poc_report_cache.clear_report_site_data(vuln_report_name)
                poc_report_cache.clear_report_analysis_report(vuln_report_name)

    @staticmethod
    def update_report() :
        report_dir = poc_operate_api.__poc_report_root_directory + vuln_report_name + local_system.get_system_directory_separator()
        
        github_api.report_tool_kit.update_report(github_organization_name + '.github.io')
    
'''
PoC Report Queue  --  Flash Vuln Data to Github
'''

class poc_report_update_queue :

    __report_update_queue = []
    __thread_lock = local_system.thread_lock()
    __update_wait_time = 30  #  update report interval is 30s
    __check_queue_interval_time = 5
    __queue_dispatch_loop = False

    class report_information :
        
        def __init__(self,report_name) :
            self.report_name = report_name
            self.entry_to_queue_time_tick = local_system.get_timetick()
    
        def get_report_name(self) :
            return self.report_name
        
        def get_timetick(self) :
            return self.entry_to_queue_time_tick
    
    @staticmethod
    def add_report(report_name) :
        new_report_information = poc_report_update_queue.report_information(report_name)
        
        poc_report_update_queue.__thread_lock.enter_lock()
        
        poc_report_update_queue.__report_update_queue.append(new_report_information)

        poc_report_update_queue.__thread_lock.exit_lock()
    
    @staticmethod
    def exit_dispatch() :
        poc_report_update_queue.__queue_dispatch_loop = False
    
    @staticmethod
    def run_dispatch() :
        if not poc_report_update_queue.__queue_dispatch_loop :  #  check dispatch thread running state ..
            local_system.create_thread(poc_report_update_queue.__queue_dispatch)
    
    @staticmethod
    def __queue_dispatch() :
        poc_report_update_queue.__queue_dispatch_loop = True
        
        while poc_report_update_queue.__queue_dispatch_loop :
#            try  #  
            current_time_tick = local_system.get_timetick()
#            local_system.debug_print('Debug Current TimeTick:' + str(current_time_tick))
            
            poc_report_update_queue.__thread_lock.enter_lock()  #  WARNING ! lock it at first will making the queue avoid rewrite
                                                                #  new report will add to queue when it call thread_lock.exit_lock()
            
            report_queue_length = len(poc_report_update_queue.__report_update_queue)
            report_queue_index  = 0
            
            while report_queue_index < report_queue_length :
                queue_report_name = poc_report_update_queue.__report_update_queue[report_queue_index].get_report_name()
                queue_time_tick = poc_report_update_queue.__report_update_queue[report_queue_index].get_timetick()
                
#                local_system.debug_print('Debug Report Name:' + queue_report_name)
#                local_system.debug_print('Debug TimeTick:' + str(queue_time_tick))
                
                if current_time_tick - queue_time_tick > poc_report_update_queue.__update_wait_time :
                    #  WARNING ! python time tick taking three decimal places 
                    #  so we don't need multiply 1000 for adject time tick to integer
                    
                    if not poc_operate_api.is_exist_report(queue_report_name) :  #  report no exist ..
                        poc_operate_api.create_report(queue_report_name)
                        
                        continue
                        
                    poc_operate_api.upload_report(queue_report_name)
                    
                    poc_report_update_queue.__report_update_queue.pop(report_queue_index)
            
                    report_queue_length -= 1
                else :
                    report_queue_index += 1
            
            poc_report_update_queue.__thread_lock.exit_lock()
            
            local_system.sleep(poc_report_update_queue.__check_queue_interval_time)
    
    
if __name__ == '__main__' :  #  test_case
    '''
    poc_report_update_queue.run_dispatch()
    poc_report_update_queue.add_report('A')
    poc_report_update_queue.add_report('B')
    poc_report_update_queue.add_report('C')
    
    import time
    
    time.sleep(5)
    
    poc_report_update_queue.exit_dispatch()
    '''
    '''
    def create_web_report(report_name,report_description = '',report_readme_information = '') :
        github_api.report_tool_kit.create_report(github_organization_name, \
                                                 github_authorization_key, \
                                                 report_name + '.github.io', \
                                                 report_description, \
                                                 report_readme_information, \
                                                 is_organization_repository = True)


    def create_normal_report(report_name,report_description = '',report_readme_information = '') :
        github_api.report_tool_kit.create_report(github_organization_name, \
                                                 github_authorization_key, \
                                                 report_name, \
                                                 report_description, \
                                                 report_readme_information, \
                                                 is_organization_repository = True)

    def delete_report(report_name) :
        github_api.report_tool_kit.delete_report(github_organization_name,github_authorization_key,report_name)
    '''

    