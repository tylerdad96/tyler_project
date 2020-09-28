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
    def get_url(self,type):
        """IB账户注册方式为通过专属链接，非邀请码"""
        if type=='IB':
            #ib代理链接,上级账号为1000003759
            self.dr.get('https://at-client-portal-uat.atfxdev.com/register?'
                        'redirect_uri=ibRebateDetail&utm_medium=ibcustomelink&'
                        'invitationCode=f42X1Bl7zKuaSG9Pyf%2FMEg%3D%3D')
        else:
            #走缺省ib分配上级
            self.dr.get('https://at-client-portal-uat.atfxdev.com/register')

    #创建存储注册数据的函数，写入已存在的本地文档中
    def saveaccount(self,excelpath,val,col,row):
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
        # 去除弹窗
        self.register_top()
        time.sleep(2)
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

    #若注册账号为ib
    def ib_table(self):
        #IB账户点击佣金申请表格
        ib_list=self.dr.find_elements_by_css_selector('.el-checkbox__inner')
        for i in ib_list[0:7]:
            i.click()
            time.sleep(1)
        self.css('div.ibRebateCon > div:nth-of-type(4) > .el-button').click()
        time.sleep(1)

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

    #判断注册页表单各字段填写是否正确
    def fill_form(self):
        try:
            erro_text=self.dr.find_elements_by_css_selector('div.el-form-item__error')
            time.sleep(1)
            for i in erro_text:
                print(i.text)
                time.sleep(1)
        except:
            pass

    #注册页必填项填写无误，查找其他错误
    def other_erro(self):
        try:
            form_erro = self.css('div.el-message--error>p').text
            print('注册失败{}'.format(form_erro))
        except:
            pass

    #登录bos
    def login_bos(self,username,psword):
        #切换语言
        self.css('.ivu-icon-ios-arrow-down').click()
        time.sleep(2)
        self.css('ul.ivu-select-dropdown-list > li:nth-of-type(2)').click()
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
        time.sleep(1)
        #输入主账户进行筛选
        self.css('div.ivu-tabs-content > div:nth-of-type(1) '
                 'div:nth-of-type(2) > div:nth-of-type(1) > '
                 'input:nth-of-type(1)').send_keys(idnum)
        time.sleep(1)
        self.css('div.ivu-tabs-content > div:nth-of-type(1) > '
                 'div:nth-of-type(1) > div:nth-of-type(1) > '
                 'div:nth-of-type(1) > div:nth-of-type(2) '
                 'div:nth-of-type(2) i:nth-of-type(1)').click()
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

    #获取手机验证码
    def get_phcode(self,idnum):
        time.sleep(2)
        self.windsw(1)
        self.dr.refresh()
        #点击简讯sms
        time.sleep(1)
        self.wcss('div.ivu-tabs-nav > div:nth-of-type(3)').click()
        time.sleep(1)
        #选择账户类型为主账户
        self.css('div.ivu-tabs-content > div:nth-of-type(2) > div:nth-of-type(1) > '
                 'div:nth-of-type(1) > div:nth-of-type(1) > '
                 'div:nth-of-type(2) span:nth-of-type(1)').click()
        time.sleep(1)
        self.css('div.ivu-select-visible .ivu-select-dropdown-list > li:nth-of-type(1)').click()
        time.sleep(1)
        self.css('div.ivu-tabs-content > \
        div:nth-of-type(2) div:nth-of-type(2) > \
        div:nth-of-type(1) > input:nth-of-type(1)').send_keys(idnum) #输入主账户
        time.sleep(1)
        self.css('div.ivu-tabs-content >div:nth-of-type(2) > \
        div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > \
        div:nth-of-type(2) div:nth-of-type(2) \
        i:nth-of-type(1)').click()
        #请求时间排序
        self.wcss('div.ivu-tabs-content > div:nth-of-type(2) th:nth-of-type(5) i:nth-of-type(2)').click()
        time.sleep(2)
        #获取最新验证码
        self.pe=self.css('div.ivu-tabs-content > div:nth-of-type(2) > div:nth-of-type(1) > \
        div:nth-of-type(1) div:nth-of-type(1) > div:nth-of-type(2) \
        tr:nth-of-type(1) a:nth-of-type(1)').text
        time.sleep(1)
        self.phonecode=re.sub('\D','',self.pe) #提取数字
        time.sleep(1)
        print('当前测试数据手机验证码:{}'.format(self.phonecode))
        return self.phonecode

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

    #上传图片
    def upload_img(self):
        self.css('div.el-form-item__content>div>div>div>p>i.la-upload').click()
        time.sleep(1)
        os.system(r'E:\test\client_kyc.exe')
        time.sleep(1)

    #验证邮箱手机
    def code_pr(self,idnumber):
        # 点击验证联系方式
        self.css('.box.progress-content > .progress-text').click()
        time.sleep(1)
        # 发送邮箱验证码
        self.css('div.el-col-24>button.dialog-sendCode').click()
        time.sleep(1)
        while True:
            # 调用函数，获取邮箱验证码
            self.get_emailcode(idnumber)
            self.windsw(0)
            time.sleep(1)
            # 输入验证码
            self.css('[placeholder="验证码"]').clear()
            time.sleep(1)
            self.css('[placeholder="验证码"]').send_keys(self.emailcode)
            time.sleep(1)
            self.css('.dialog-submit').click()  # 点击下一步
            # 判断邮箱是否验证成功
            self.emsu = self.css('.is-success.el-step__title').text
            time.sleep(1)
            print(self.emsu)
            time.sleep(1)
            self.css('.dialog-sendCode').click()
            if self.emsu == '电邮验证成功':
                # 发送手机验证码
                self.get_phcode(idnumber)
                time.sleep(1)
                self.windsw(0)
                self.css('[placeholder="验证码"]').clear()
                time.sleep(1)
                self.css('[placeholder="验证码"]').send_keys(self.phonecode)
                time.sleep(1)
                self.css('.dialog-submit').click()
                time.sleep(1)
                self.css('button.dialog-submit > span').click()
                break
            else:
                continue

    #判断kyc表单填写是否错误
    def kycerro(self):
        try:
            self.css('div.el-card__body>h2')
            return True
        except:
            return False

    #填写kyc表单
    def kyc_form(self,country,fistname,lastname):
        #点击首页
        self.css('button.side-nav-cell .menu-font').click()
        time.sleep(1)
        #填写资讯
        self.css('div.nav > div:nth-of-type(4) .progress-text').click()
        time.sleep(1)
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
        # 随机输入电话号码
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
        self.css('label.agree-rules-box .el-checkbox__inner').click()
        time.sleep(1)
        self.css('button.submit-btn > span').click()
        time.sleep(1)

    #kyc认证
    def kycfulfill(self,idnum,country,fistname,lastname):
        #手机邮箱验证
        self.code_pr(idnum)
        while True:
            time.sleep(2)
            #KYC表格填写
            self.kyc_form(country,fistname,lastname)
            if self.kycerro():
                self.css('button.side-nav-cell .menu-font').click()
                break
            else:
                continue

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
            time.sleep(1)
            js_top="var q=document.documentElement.scrollTop=0"
            #回到顶部
            self.dr.execute_script(js_top)
            # 初审处理中
            self.css('button.ivu-btn-default>span>span').click()
            time.sleep(1)
            # 成功初审
            self.css('div.application-wrap .ivu-dropdown-menu > li:nth-of-type(1)').click()
            time.sleep(1)
        else:
            #初审处理中
            self.css('button.ivu-btn-default>span>span').click()
            time.sleep(1)
            #成功初审
            self.css('div.application-wrap .ivu-dropdown-menu > li:nth-of-type(1)').click()
            time.sleep(1)
            #选择账户区域
            self.mt_group=self.dr.find_elements_by_css_selector('div.ivu-select-default>'
                                                             'div.ivu-select-selection>div>input.ivu-select-input')
            self.mt_group[1].click()
            time.sleep(1)
            self.css('div.ivu-select-visible li:nth-of-type(4)').click()
            time.sleep(1)
            #选择组别
            self.mt_group[2].click()
            time.sleep(1)
            self.css('div.ivu-select-visible li:nth-of-type(3)').click()

        #输入随机邮编
        time.sleep(1)
        you=self.dr.find_elements_by_css_selector('form.ivu-form-label-top>div.ivu-row>div.ivu-col-span-12>div>div.ivu-form-item-required>div.ivu-form-item-content>div.ivu-input-wrapper>input')
        you[1].send_keys(''.join(random.sample('0123456789', 8)))
        time.sleep(1)
        #确定
        self.css('div.ivu-modal-footer>div>button.ivu-btn-primary').click()
        time.sleep(2)
        #获取交易账户
        js_dowmt = "var q=document.documentElement.scrollTop=10000"
        self.dr.execute_script(js_dowmt)#回到底部
        time.sleep(2)
        #真实交易账信息
        self.css('div#tdAccount > .ivu-collapse-header').click()
        time.sleep(1)

    def save_msg(self,subp,excelpath):
        #获取交易账户信息并写入本地文档
        for i in [1,3,4,5]:
            idmsg=self.dr.find_element_by_xpath('//*[@id="tdAccount"]/div[2]/div/'
                                      'div/div[3]/div[1]/div[2]/table/tbody/tr/td[{}]/div/div/span'.format(i)).text
            time.sleep(1)
            if i==1:
                self.saveaccount(excelpath,idmsg,'D',subp+2)
                print('交易账号：{}'.format(idmsg))
            elif i==3:
                self.saveaccount(excelpath,idmsg,'E',subp+2)
                print('伺服务器名称：{}'.format(idmsg))
            elif i==4:
                self.saveaccount(excelpath,idmsg,'F',subp+2)
                print('组别：{}'.format(idmsg))
            else:
                self.saveaccount(excelpath,idmsg,'G',subp+2)
                print('状态：{}'.format(idmsg))