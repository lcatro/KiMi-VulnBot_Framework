
#### KiMi-VulnBot PoC Plugin

 这是KiMi-VulnBot PoC 扫描插件目录,用于提供PoC 扫描插件到`poc_framework_scan_plugin.py` 运行<br/>


#### PoC 文件命名

 Plugin 插件以`__poc_` 为前缀,方便于`poc_framework_scan_plugin.py` 识别扫描框架<br/>

#### PoC 接口

 Plugin 插件接口做到尽量精减,只需要PoC Plugin 模块提供`valid_vuln()` 函数即可<br/>

```py
def valid_vuln(host,port,other = {}) :
    #  poc valid code 
    # ...
    
    return boolen_value
```

 `valid_vuln()`函数有三个参数:<br/>
 `host`  当前要测试的host/ip 地址<br/>
 `port`  当前要测试的端口<br/>
 `other` 拓展参数<br/>

 当前目录下的`poc_temllete.py` 是关于S2-046 的扫描框架例子<br/>
