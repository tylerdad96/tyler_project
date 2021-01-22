# from selenium import webdriver

# options=webdriver.ChromeOptions()
# options.add_argument('lang=zh_CN.UTF-8')
# options.add_argument('--incognito')
# options.add_argument('--start-maximized')

# driver=webdriver.Chrome(chrome_options=options)
# driver.get('https://www.baidu.com/')
# import logging
# def logout(name):
#     # 先创建一个logger
#     logger = logging.getLogger(name)  # 定义Logger的名字，之前直接用logging调用的名字是root，日志格式用%(name)s可以获得。这里的名字也可以自定义比如"TEST"
#     logger.setLevel(logging.DEBUG)  # 低于这个级别将被忽略，后面还可以设置输出级别
#     # 创建handler和输出级别
#     ch = logging.StreamHandler()  # 输出到屏幕的handler
#     ch.setLevel(logging.INFO)  # 输出级别和上面的忽略级别都不一样，可以看一下效果

#     # 创建日志格式，可以为每个handler创建不同的格式
#     ch_formatter = logging.Formatter('%(name)s %(asctime)s {%(levelname)s}:%(message)s',datefmt='%Y-%m-%d %H:%M:%S')  # 关键参数datefmt自定义日期格式

#     # 把上面的日志格式和handler关联起来
#     ch.setFormatter(ch_formatter)

#     # 将handler加入logger
#     logger.addHandler(ch)

#     return logger

# logout('test').info('thuehhth')
# # # 以上就完成了，下面来看一下输出的日志
# # logger.debug('logger test debug')
# # logger.info('logger test info')
# # logger.warning('logger test warning')
# # logger.error('logger test error')
# # logger.critical('logger test critical')

from browser_actions import Commonweb
import time

c=Commonweb()
c.open_browser()
c.open_web('https://www.baidu.com/')
time.sleep(2)
c.double_click('css,.hot-refresh-text')
time.sleep(3)
c.suspension('css,.s-top-right-text')
c.display_findelement('css,#kw').send_keys(13)

# import os
# import time
# print(os.getcwd())
# pictour_dir=os.path.join(os.sys.path[0],'pictour')
# print(pictour_dir)
# # pict_name=time.strftime('%Y-%m-%d-%H.%M.%S',time.localtime(time.time()))
# # print(pict_name)
# # pri_path=os.path.join(os.path.join(os.getcwd(),'pictour'),time.strftime('%Y-%m-%d-%H.%M.%S',time.localtime(time.time())))
# # print(pri_path)

# print(os.sys.path[0]) #上级目录
# print(os.__file__)
# print(os.path.abspath(__file__))
# os.mkdir('pictour')
# pict_path=os.path.join(os.sys.path[0],'picture')
# if not os.path.exists(pict_path):
#     os.mkdir(pict_path)
# pict_name=os.path.join(pict_path,'{}.png'.format(54564))
# print(pict_name)
# # print(pict_path)
# # print(os.path.exists('D:\master\pictour'))

# def test(a):
#     return a+1
    

# c=lambda a:a+2
# print(c(2))

# def c(a):
#     return c+2

# d=lambda y:test(y)
# print(d(6))