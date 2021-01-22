"""公共方法及变量释义"""
///
browser_actions.py 模块:
公共方法:
    open_browser(browsername='Chrome')       打开浏览器，默认为谷歌浏览器
    open_web(url)                            访问url
    find_element(locator,index=0)            定位页面元素(无论是否唯一)，默认下标为0
    web_input(locator,values,index=0)        页面输入
    web_click(locator,index=0)               页面点击
    double_click(locator,index=0)            页面双击
    suspension(locator,index=0)              鼠标悬浮
    get_screenpict(filename)                 截图当前页面
    close_browser()                          关闭浏览器
    quit_browser()                           退出浏览器进程

变量:
browsername:浏览器名称 如Firefox、Chrome
url：访问域名
locator：定位方法及元素值，格式‘定位方法，元素值’如 'css,#kw'
index：下标
values：输入的值
filename：文件夹名称


other_actions.py 模块:
公共方法:
log_output(name)                             自定义日志输出

name:错误日志名称
///
