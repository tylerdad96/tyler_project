import logging

"""此模块用于存放公共方法"""
class public_method():
    
    #创建日志函数，打印日志报告,错误级别：debug、info、warning、error、critical
    def log_output(self,name): #参数name为日志名字
        #创建一个logger
        self.logger = logging.getLogger(name) #定义Logger的名字，之前直接用logging调用的名字是root，日志格式用%(name)s可以获得。这里的名字也可以自定义比如"TEST"
        self.logger.setLevel(logging.DEBUG) #低于这个级别将被忽略，后面可以设置输出级别
        # 创建handler和输出级别
        self.output_log = logging.StreamHandler()  # 输出到屏幕的handler
        self.output_log.setLevel(logging.INFO)  # 输出级别和上面的忽略级别都不一样，可以看一下效果
        # 关键参数datefmt自定义日期格式    
        self.ch_formatter = logging.Formatter('%(name)s %(asctime)s {%(levelname)s}:%(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        # 把上面的日志格式和输出到屏幕的handler关联起来
        self.output_log.setFormatter(self.ch_formatter)
        # 将handler加入logger
        self.logger.addHandler(self.output_log)
        #返回输出日志级别
        return self.logger




