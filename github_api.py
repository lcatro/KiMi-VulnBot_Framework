
#cofing :utf-8

import json
import os
import requests

import local_system


class report_tool_kit :

    class git_api :
        
        @staticmethod
        def get_auth_headers(github_authorization_key) :
            headers = {
                'Authorization' : 'token ' + github_authorization_key
            }

            return headers

        @staticmethod
        def create_user_repository(github_repository_name,github_authorization_key,repository_description = '',repository_homepage = '') :
            upload_repository_attributes = {
              'name' : github_repository_name ,
              'description' : repository_description ,
              'homepage' : repository_homepage ,
            }

            status_code = requests.post('https://api.github.com/user/repos' ,
                                   headers = report_tool_kit.git_api.get_auth_headers(github_authorization_key) ,
                                   json = upload_repository_attributes
                                  ).status_code

            if 200 == status_code :
                return True

            return False

        @staticmethod
        def create_organization_repository(github_organization_name,github_repository_name,github_authorization_key,repository_description = '',repository_homepage = '') :
            upload_repository_attributes = {
              'name' : github_repository_name ,
              'description' : repository_description ,
              'homepage' : repository_homepage ,
            }

            status_code = requests.post('https://api.github.com/orgs/' + github_organization_name + '/repos' ,
                                   headers = report_tool_kit.git_api.get_auth_headers(github_authorization_key) ,
                                   json = upload_repository_attributes
                                  ).status_code

            if 200 == status_code :
                return True

            return False

        @staticmethod
        def delete_user_repository(github_repository_name,github_user_name,github_authorization_key) :
            status_code = requests.delete('https://api.github.com/repos/' + github_user_name + '/' + github_repository_name ,
                                     headers = report_tool_kit.git_api.get_auth_headers(github_authorization_key)
                                    ).status_code

            if 204 == status_code :
                return True

            return False

        @staticmethod
        def delete_organization_repository(github_organization_name,github_repository_name,github_authorization_key) :
            status_code = requests.delete('https://api.github.com/repos/' + github_organization_name + '/' + github_repository_name ,
                                     headers = report_tool_kit.git_api.get_auth_headers(github_authorization_key)
                                    ).status_code

            if 204 == status_code :
                return True

            return False

    class git_shell :

        def __init__(self,report_directory_path) :
            if not local_system.is_exist_directory(report_directory_path) :
                raise ValueError,'GitShell open unexist report_directory_path :' + report_directory_path
                
            self.report_directory_path = report_directory_path

        def entry_repository_directory(self) :
            os.chdir(self.report_directory_path)

        def exit_repository_directory(self) :
            os.chdir(local_system.get_current_path())

        def init_repository_directory(self) :
            os.system('git init')

        def add_repository_all_file(self) :
            os.system('git add .')

        def add_repository_file(self,file_path) :
            os.system('git add ' + file_path)

        def commit_repository(self,commit_information = '.') :
            os.system('git commit -m "' + commit_information + '"')

        def set_remote_repository_origin(self,origin_link) :
            os.system('git remote add origin ' + origin_link)

        def set_http_remote_repository_origin_by_name(self,origin_user_or_organization_name,repository_name) :
            os.system('git remote add origin https://github.com/' + origin_user_or_organization_name + '/' + repository_name + '.git')

        def set_ssh_remote_repository_origin_by_name(self,origin_user_or_organization_name,repository_name) :
            os.system('git remote add origin git@github.com:' + origin_user_or_organization_name + '/' + repository_name + '.git')

        def push_repository(self,argument_string = '') :
            os.system('git push ' + argument_string)

        def push_to_repository_master(self,argument_string = '') :
            self.push_repository('-u origin master')
    
        def pull_repository_directory(self) :
            os.system('git pull')

    @staticmethod
    def __make_new_file(file_name,file_data = '') :
        file = open(file_name,'w')
        
        if not file_data == '' :
            file.write(file_data)
            
        file.close()
        
    
    @staticmethod
    def create_report(github_user_or_organization_name,github_authorization_key,report_name,report_description = '',report_readme_information = '',is_organization_repository = False) :
        if is_organization_repository :
            report_tool_kit.git_api.create_user_repository(report_name,github_authorization_key,report_description)
        else :
            report_tool_kit.git_api.create_organization_repository(github_user_or_organization_name, \
                                                                   report_name, \
                                                                   github_authorization_key, \
                                                                   report_description)
        
        if not os.path.isdir(report_name) :
            os.mkdir(report_name)
            report_tool_kit.__make_new_file(report_name + '/README.md',report_readme)
    
        repository = report_tool_kit.git_shell(report_name)
        
        repository.entry_repository_directory()
        repository.init_repository_directory()
        repository.add_repository_all_file()
        repository.commit_repository()
        repository.set_ssh_remote_repository_origin_by_name(github_user_name,github_test_repository_name)
        repository.push_to_repository_master()
        repository.exit_repository_directory()
    
    @staticmethod
    def delete_report(github_user_or_organization_name,github_authorization_key,github_repository_name) :
        report_tool_kit.git_api.delete_user_repository(github_repository_name,github_user_or_organization_name,github_authorization_key)
    
    @staticmethod
    def upload_report(github_repository_name) :
        repository = report_tool_kit.git_shell(github_repository_name)
        
        repository.entry_repository_directory()
        repository.add_repository_all_file()
        repository.commit_repository()
        repository.push_repository()
        repository.exit_repository_directory()
    
    @staticmethod
    def update_report(github_repository_name) :
        repository = report_tool_kit.git_shell(github_repository_name)
        
        repository.entry_repository_directory()
        repository.pull_repository_directory()
        repository.exit_repository_directory()
    

if __name__ == '__main__' :  #  test case ..
    '''
    github_organization_name = 'KiMiThreatPerception'
    github_user_name = 'KiMi-VulnBot'
    github_authorization_key = '7292ffb88b91efd93f243a736a45d439596cd99c'
    github_test_repository_name = 'test'#'Hello-World'
    '''
#    report_tool_kit.delete_report(github_user_name,github_authorization_key,github_test_repository_name)
#    report_tool_kit.create_report(github_user_name,github_authorization_key,github_test_repository_name,'Just Test ! ..')

    '''
    is_create = True

    if not is_create :
        report_tool_kit.git_api.delete_user_repository(github_test_repository_name,github_user_name,github_authorization_key)
    else :
#        os.remove('test/.git')
        report_tool_kit.git_api.create_user_repository(github_test_repository_name,github_authorization_key,'test project..')
    
        repository = git_shell(github_test_repository_name)
        repository.entry_repository_directory()
        repository.init_repository_directory()
        print 'init_repository_directory'
        repository.add_repository_all_file()
        print 'add_repository_all_file'
        repository.commit_repository('first commit')
        print 'commit_repository'
        repository.set_ssh_remote_repository_origin_by_name(github_user_name,github_test_repository_name)
        print 'set_remote_repository_origin_by_name'
        repository.push_to_repository_master()
        print 'push_to_repository_master'
    '''
#    report_tool_kit.git_api.create_user_repository(github_test_repository_name,github_authorization_key,'test')
#    create_organization_repository(github_organization_name,github_test_repository_name,github_authorization_key)
#    delete_organization_repository(github_organization_name,github_test_repository_name,github_authorization_key)

#    init_repository_directory('./test')
