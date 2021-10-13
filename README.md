# ZhihuTop

第一次从app上抓取数据

第一部分
__init__
包含的url为抓取的api接口，headers就不解释了

第二部分
get_data
通过requests的get请求获取到数据并赋给变量response
接着通过json模块把数据转为字典
返回 数据

第三部分
parse_data
把数据整理分类保存到字典
通过循环每次重新赋值字典的键和值
最后把字典数据添加到列表里

第四部分
save
保存

main启动
通过schedule模块每天自动抓取


end.
