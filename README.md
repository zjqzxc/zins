# zins
Zins is not Srun

##简短介绍：
  主页http://zins.flagplus.net/
  <br />目前共提供三个版本，男生版，女生版，命令行版。开发时绝大多数时间用在女生版，男生版在女生版的基础上略有改动形成。命令行版功能相对较弱，原因嘛，有些功能实现起来实在是不方便呀。

##使用说明：
####方法一：从源码执行
  该版本目前仅支持python3，Linux系统下使用需另行安装python3及tkinter库。
  <br />直接执行zinsGUI_B.py 或 zinsGUI_G.py即可使用
####方法二：使用二进制版本
  下载：http://pan.baidu.com/s/1i3ncEUh  包含历史版本，建议使用最新版。
  <br />下载所需版本，解压后执行zinsGUI_B.exe或zinsGUI_G.exe即可。如需命令行版请执行zinsc.exe（男生版及女生版均包含命令行版）
  
####使用Py2exe打包：（仅限于Windows系统，并确保py2exe已安装）
  直接执行GUISetup.bat即可自动完成打包操作。
  <br />GUIB_setup.py、GUIG_setup.py、CMD_setup.py分别为男生版，女生版及命令行版的打包文件，单独打包某一版本可使用类似python CMD_setup.py py2exe的命令进行。
  

##更新历史
####1.10 Alpha
+ 重写mainclass.py，将IPv4与IPv6操作函数统一，以参数方式区分
+ 重写命令行版，增加注销功能
+ 修正部分界面BUG
+ 该版本目前仍存在较多问题，需要严格测试，不发布二进制版

###1.03
+ 修复上一版本IPv6不可用时软件报错无法启动的BUG（严重）
+ 新增IPv6及IPv4不可用时禁用复选矿功能以防止意外

###1.02
+ 新增IPv6检测功能
+ 修改IPv6登陆信息记录部分，使其与IPv4区分，以应对IPv4与IPv6服务器时间戳不一致

###1.0.1 Alpha
+ 新增：IPv6登陆注销保持在线支持
+ 男生版新增详细信息显示功能，可显示已用流量，实时网速等信息
 
###1.0.0 Alpha
+ 提供了最基础的登陆注销以及保持在线功能
+ IPv6暂不支持