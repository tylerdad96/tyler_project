from selenium.webdriver.support.wait import WebDriverWait
from openpyxl import load_workbook
import time
import re
import os
from selenium.webdriver.common.action_chains import ActionChains
import random
from selenium.webdriver.common.keys import Keys

class basepage():
    """对selenium二次封装，定义一个所有脚本都继承的类，封装基本方法，尽量将元素定位放在此类中"""
    def __init__(self,driver):
        self.dr=driver
        self.dr.maximize_window()
        self.dr.implicitly_wait(20)

    #封装css定位
    def css(self,css):
        return self.dr.find_element_by_css_selector(css)

    #封装显示等待定位
    def wcss(self, name):
        return WebDriverWait(self.dr, 10, 1).until(lambda x: x.find_element_by_css_selector(name))

    #封装访问地址，根据账户类型访问不同url
    def get_url(self,link,code,n):
        """判断是通过专属链接还是邀请码注册"""
        if len(link)!=0:
            #通过ib专属链接注册
            self.dr.get(link)
            #去除弹窗
            self.register_top()
            self.saveaccount(r'E:\test\account_number.xlsx', '专属链接', 'F', n)
        else:
            #通过邀请码
            self.dr.get('https://at-client-portal-uat-proxy.ntdevops.com/register')
            time.sleep(1)
            #去除弹窗
            self.register_top()
            time.sleep(1)
            self.css('div.el-form-item__content>div.invitationCode-input>textarea').send_keys(code)
            self.saveaccount(r'E:\test\account_number.xlsx', '邀请码', 'F', n)

    # 创建存储注册数据的函数，写入已存在的本地文档中
    def saveaccount(self, excelpath, val, col, row):
        """注：调用此函数时，不能打开需要写入数据的文档"""
        workbook = load_workbook(filename=excelpath)
        sheet = workbook.active
        cel = sheet['{}{}'.format(col, row)]
        cel.value = val
        workbook.save(filename=excelpath)

    #判断注册国家是否为uk国家
    def is_uk(self,country):
        self.uk_list=['阿尔巴尼亚','安道尔','奥地利','波斯尼亚和黑塞哥维那','保加利亚','克罗地亚','塞浦路斯','捷克共和国',
                      '丹麦','爱沙尼亚','芬兰','佐治亚州','德国','直布罗陀','希腊','匈牙利','冰岛','爱尔兰','意大利',
                      '拉脱维亚','列支敦士登','立陶宛','卢森堡','马其顿','马耳他','摩纳哥','黑山共和国','荷兰','挪威',
                      '葡萄牙','塞尔维亚共和国','罗马尼亚','圣马力诺','斯洛伐克','斯洛文尼亚','西班牙','西班牙','瑞典','瑞士','英国']
        if country in self.uk_list:
            print('AT Global Markets Limited 不接受居住在这个国家的个人申请。')
            return True
        else:
            return False

    #注册页面表单
    def register_form(self,ISO,country,email,testname,psword):
        time.sleep(1)
        # 选择语言为简体中文
        self.register_cn()
        # 名字字段引用测试文档中的三字码，此处需要用到数据驱动
        self.css('[placeholder="名字"]').send_keys(ISO)
        time.sleep(1)
        # 姓氏
        self.css('[placeholder="姓氏"]').send_keys(testname)
        # 居住国家选择测试文档中的国家
        self.css('[placeholder="选择居住国家"]').click()
        time.sleep(1)
        self.dr.find_element_by_xpath('//span[.="{}"]'.format(country)).click()
        time.sleep(1)
        # 输入联通手机号码
        self.phone_list = [130, 131, 132, 155, 156, 185, 186, 145, 146, 166, 167, 175, 176]
        self.phone_num = str(random.choice(self.phone_list)) + ''.join(random.sample('0123456789', 8))  # 随机生成联通号码
        self.css('[placeholder="手机号码"]').send_keys(self.phone_num)
        time.sleep(1)
        # 输入邮箱
        self.css('[placeholder="电子信箱"]').send_keys(email)
        time.sleep(1)
        # 输入密码
        self.css('[placeholder="会员账户密码"]').send_keys(psword)
        time.sleep(1)
        # 输入万能验证码
        self.css('[placeholder="验证码"]').send_keys('R0sLRl/E2wOcQ/lrejVuabwi9zOnoWCoLrV7yTduyEI=')
        time.sleep(1)
        # 点击下一步
        self.css('button.el-button > span').click()
        time.sleep(2)

    #代理申请
    def ib_apply(self):
        self.css('div.el-dialog__footer>div>button.el-button--primary').click()

    #ib返佣申请表格
    def ib_table(self):
        time.sleep(1)
        ib_list=self.dr.find_elements_by_css_selector('.el-checkbox__inner')
        time.sleep(2)
        print(len(ib_list))
        if len(ib_list)<=2:
            self.css('div.ps-agree-bot .el-checkbox__inner').click()
            time.sleep(1)
        else:
            for i in ib_list[0:random.randint(1,len(ib_list)-2)]:
                i.click()
                time.sleep(1)
            self.css('div.ps-agree-bot .el-checkbox__inner').click()
        time.sleep(1)
        self.css('div.ibRebateCon > div:nth-of-type(4) > .el-button').click()

    #显示等待获取页面文本
    def page_text(self,element):
        self.t=self.wcss(element).text
        return self.t

    #去除登录页面的弹窗
    def register_top(self):
        # 如果有警告框，则点击，否则pass
        try:
            self.wcss('.blk-sure-btn').click()
        except:
            pass

    #会员登录注册页中心弹窗
    def register_cn(self):
        #选择语言为简体中文
        self.css('.la-globe').click()
        time.sleep(1)
        self.css('ul.el-dropdown-menu > li:nth-of-type(2)').click()
        time.sleep(1)

    #去除首次登录会员中心的弹窗
    def login_top(self):
        #去除弹窗
        self.wcss('div.text-center .el-checkbox__inner').click()
        time.sleep(1)
        self.css('.confirm-btn').click()
        time.sleep(2)

    #登录bos
    def login_bos(self,username,psword):
        #切换语言
        self.css('.ivu-icon-ios-arrow-down').click()
        time.sleep(2)
        self.css('ul.ivu-select-dropdown-list > li:nth-of-type(1)').click()
        #登录bos账户
        self.css('[placeholder="账号"]').send_keys(username)
        time.sleep(1)
        self.css('[placeholder="密码"]').send_keys(psword)
        time.sleep(1)
        self.css('button.ivu-btn-large > span').click()

    #窗口切换
    def windsw(self,n):
        self.all_handles = self.dr.window_handles
        #n=0切换到会员中心，n=1切换到bos
        return self.dr.switch_to.window(self.all_handles[n])

    def get_emailcode(self,idnum):
        #切换窗口
        self.windsw(1)
        #进入邮箱短信页面
        self.wcss('div[width="200"] li:nth-of-type(5) > .ivu-menu-submenu-title > span').click()
        time.sleep(1)
        self.wcss('div[width="200"] [href="/report/emailrecord"]').click()
        time.sleep(2)
        #输入主账户进行筛选
        self.css('div.ivu-input-wrapper-default>input').send_keys(idnum)
        time.sleep(1)
        self.css('div.ivu-input-wrapper-default>div.ivu-input-group-append>button>i.ivu-icon-ios-search').click()
        time.sleep(1)
        #按发送时间排序
        self.css('div.ivu-tabs-content > div:nth-of-type(1) th:nth-of-type(5) i:nth-of-type(2)').click()
        time.sleep(1)
        #获取最新的验证码
        try:
            self.dr.find_element_by_xpath('//div[@class="ivu-tabs-content"]//tr[1]/td[3]').click()
        except:
            time.sleep(2)
            self.dr.refresh()
            self.dr.find_element_by_xpath('//div[@class="ivu-tabs-content"]//tr[1]/td[3]').click()
        time.sleep(2)
        self.e = self.dr.find_elements_by_xpath('//div[@class="ivu-drawer-wrap"]//tr[2]//tr[4]/td[1]/span')
        self.t = self.e[0].text
        # 输出验证码
        self.emailcode=re.sub('\D','',self.t) #提取数字
        print('当前测试数据邮箱验证码:{}'.format(self.emailcode))
        return self.emailcode

    def login_cl(self,email,pasword):
        # 选择简体中文
        time.sleep(2)
        self.css('.la-globe').click()
        time.sleep(2)
        self.css('ul.el-dropdown-menu > li:nth-of-type(2)').click()
        # 输入邮箱
        self.css('[placeholder="请输入您的电子信箱"]').send_keys(email)
        time.sleep(1)
        # 输入密码
        self.css('div.formBlock > .el-form > .el-col [placeholder="请输入您的密码"]').send_keys(pasword)
        time.sleep(1)
        # 点击登录
        self.css('div.formBlock > .el-form > .el-col .el-button').click()
        time.sleep(3)

    def login_cl(self,email,pasword):
        # 选择简体中文
        time.sleep(2)
        self.css('.la-globe').click()
        time.sleep(2)
        self.css('ul.el-dropdown-menu > li:nth-of-type(2)').click()
        # 输入邮箱
        self.css('[placeholder="请输入您的电子信箱"]').send_keys(email)
        time.sleep(1)
        # 输入密码
        self.css('div.formBlock > .el-form > .el-col [placeholder="请输入您的密码"]').send_keys(pasword)
        time.sleep(1)
        # 点击登录
        self.css('div.formBlock > .el-form > .el-col .el-button').click()
        time.sleep(3)

    #填写kyc表单
    def kyc_form(self,country,fistname,lastname):
        # 选择证件签发国
        self.css('[placeholder="请选择您的证件签发国"]').click()
        time.sleep(1)
        self.lssue = self.dr.find_elements_by_xpath('//span[.="{}"]'.format(country))
        time.sleep(1)
        self.lssue[0].click()
        time.sleep(1)
        # 上传图片
        self.upload_img()
        time.sleep(1)
        # 随机选择性别
        sex = self.dr.find_elements_by_css_selector('label.el-radio>span>span.el-radio__inner')
        sex[random.choice([0, 1])].click()
        time.sleep(1)
        #输入姓名
        self.css('[placeholder="请输入真实姓氏"]').send_keys(fistname)
        time.sleep(1)
        self.css('[placeholder="请输入真实名字"]').send_keys(lastname)
        # 随机选择出生日期
        self.css('[placeholder="请选择出生日期为DD-MM-YYYY的格式"]').click()
        time.sleep(1)
        self.css('div.el-date-picker__header > span:nth-of-type(1)').click()
        # 年份
        selty = self.dr.find_element_by_css_selector('.el-icon-d-arrow-left')
        ActionChains(self.dr).double_click(selty).perform()  # 双击
        selty.click()
        time.sleep(1)
        by = self.dr.find_elements_by_css_selector('table.el-year-table>tbody>tr>td')
        by[random.randint(0, 9)].click()
        time.sleep(1)
        # 月份
        bm = self.dr.find_elements_by_css_selector('table.el-month-table>tbody>tr>td')
        bm[random.randint(0, 11)].click()
        time.sleep(1)
        # 日期
        bd = self.dr.find_elements_by_css_selector('table.el-date-table>tbody>tr>td')
        bd[random.randint(0, 41)].click()
        time.sleep(1)
        # 随机输入证件号码
        self.css('[placeholder="请输入证件号码"]').send_keys(''.join(random.sample('0123456789', 8)))
        time.sleep(1)
        # 选择居住地为文档中的证件签发国
        self.css('[placeholder="请选择现居地"]').click()
        time.sleep(2)
        ju = self.dr.find_elements_by_xpath('//span[.="{}"]'.format(country))
        time.sleep(1)
        ju[1].click()
        time.sleep(1)
        # 输入随机地址
        self.css('[placeholder="请输入地址"]').send_keys(''.join(random.sample('ABCDEFGHIJKLMN', 8)))
        #接受条款
        self.css('label.agree-checkbox>span.el-checkbox__input>span.el-checkbox__inner').click()
        time.sleep(1)
        self.css('button.submit-btn > span').click()
        time.sleep(1)

    #kyc认证
    def kycfulfill(self,idnum,country,fistname,lastname):
        #手机邮箱验证
        self.code_pr(idnum)
        time.sleep(2)
        #KYC表格填写
        self.kyc_form(country,fistname,lastname)
        time.sleep(1)
        self.css('button.side-nav-cell .menu-font').click() #回到首页

    #初审操作，指派，开户等
    def review_success(self,idnumber):
        #点击客户管理
        self.css('div.ivu-menu-submenu-title>span.ivu-badge>span').click()
        time.sleep(1)
        #点击客户请求
        self.css('div[width="200"] [href="/client/clientRequest"] > .ivu-badge >span').click()
        time.sleep(1)
        #输入主账户查询
        self.css('div.ivu-input-group > [placeholder]').send_keys(idnumber)
        time.sleep(1)
        self.css('button.ivu-btn-icon-only > .ivu-icon').click()
        time.sleep(1)
        #指派
        self.css('button.ivu-btn-small > span').click()
        time.sleep(1)
        self.css('div.btn-group > button:nth-of-type(1) > span').click()
        #回到客户名单
        self.css('li.ivu-menu-child-item-active>ul.ivu-menu>a.ivu-menu-item>span').click()
        time.sleep(1)
        #搜索主账户
        self.css('div.ivu-input-group-with-append > [placeholder]').send_keys(idnumber)
        time.sleep(1)
        self.css('button.ivu-btn-icon-only > .ivu-icon').click()
        time.sleep(1)
        self.dr.find_element_by_xpath('//a[.="{}"]'.format(idnumber)).click()
        time.sleep(2)
        #获取所有句柄
        hadl=self.dr.window_handles
        #切换窗口
        self.dr.switch_to.window(hadl[1])
        time.sleep(1)
        #判断账户类型是否存在返佣表格,10开头为ib账户，12为cl账户
        if idnumber[0:2]=='10':
            #滚动到底部
            js_dowm = "var q=document.documentElement.scrollTop=10000"
            self.dr.execute_script(js_dowm)
            time.sleep(1)
            #点击返佣申请
            self.css('div#ibRebate > .ivu-collapse-header').click()
            time.sleep(1)
            #点击审核开关
            self.css('div.left-btn>span.ivu-switch-default').click()
            time.sleep(1)
            self.css('div.ivu-modal-confirm-footer > .ivu-btn-primary').click()
            time.sleep(1)
            #修改代理代码
            ib_some = self.dr.find_elements_by_css_selector('div.input-item-page-enabled>div>div.item-text')
            ActionChains(self.dr).double_click(ib_some[0]).perform()  # 双击
            time.sleep(1)
            ib_input=self.css('.ivu-input-small')
            ib_input.send_keys(Keys.CONTROL,'a')
            time.sleep(1)
            ib_input.clear() #清空
            time.sleep(1)
            #输入随机IB代理代码
            ib_input.send_keys(''.join(random.sample('ABCDEFGHIJKLMN', 6))+'TYLERIB')
            time.sleep(1)
            self.css('.ivu-icon-md-checkmark').click()
            time.sleep(2)
            #选择代理链接
            time.sleep(1)
            ib_link=self.css('div.input-item-page-enabled .ivu-icon')
            ActionChains(self.dr).double_click(ib_link).perform()#双击
            time.sleep(1)
            self.css('.ivu-select-multiple.ivu-select [placeholder="请选择"]').click()
            time.sleep(1)
            #选择代理链接
            self.css('div.ivu-select-dropdown-transfer li:nth-of-type(3)').click()
            time.sleep(1)
            #点击空白处
            self.css('.user-status').click()
            time.sleep(1)
            # 点击确定
            self.css('.ivu-icon-md-checkmark').click()
        else:
            pass