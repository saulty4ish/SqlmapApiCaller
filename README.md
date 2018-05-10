# SqlmapApiCaller
调用sqlmap api批量检测get型sql注入


使用方式：

1.打开sqlmapapi(kali下在/usr/share/sqlmap下)：

python sqlmapapi.py -s 

2.导入要批量检测的url进input.txt

3.运行脚本：

python SqlmapApiCaller.py



代码说明：

没啥特色，因为需要给sqlmap时间去跑，

所以每5s询问一次api是否完成，询问20次也就是100s，如果没有完成则放弃。

可以自己调整count的判断条件


Tips:

1.sqlmap检测有一些显然没有注入的网址也要很久，最好用一些工具粗检测一遍再导进sqlmap跑，效率更高。


萌新的渣代码，求star求鼓励....





