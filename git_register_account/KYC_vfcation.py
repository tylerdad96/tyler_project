#导包
from selenium import webdriver
import time
from country_list import exceldata
import ddt
import unittest
from BeautifulReport import BeautifulReport
from public import basepage

#提取前面脚本注册成功后的数据
e=exceldata()
rows=e.openexcel(r'E:\test\account_number.xlsx','Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()


@ddt.ddt#数据驱动
class kyc_verification(unittest.TestCase,basepage):
    """2.0会员中心的验证码及KYC验证"""
    def setUp(self):  # 预置条件,注册销售/代理，更改链接即可
        self.dr = webdriver.Chrome()
        #实例化父类
        self.pub = basepage(self.dr)
        self.dr.get('https://at-client-portal-uat.atfxdev.com/login')
        self.register_top()
        time.sleep(2)
        #js打开新窗口访问bos
        js = 'window.open("https://at-bos-frontend-uat.atfxdev.com/login")'
        self.dr.execute_script(js)
        #切换到bos窗口
        self.windsw(1)
        time.sleep(2)
        #登录bos
        self.login_bos('tyler','Tl123456')

    def tearDown(self):  # 环境恢复
        self.dr.close()
        self.dr.quit()

    @ddt.data(*testdata)
    def test_verification(self,data):
        """KYC资料填写"""
        # 测试数据下标
        self.subp = testdata.index(data)
        print('当前测试数据：邮箱:{}，主账户:{}，证件签发国:{}'.format(data['邮箱'],data['主账户'],data['证件签发国']))
        self.windsw(0)
        #登录会员中心
        self.login_cl(data['邮箱'],'Tl123456')
        #填写kyc认证表单
        self.kycfulfill(data['主账户'],data['证件签发国'],'Tylertest',data['三字码'])
        resucess=self.css('div.nav > div:nth-of-type(4) .verify-status-txt').text
        if resucess=='等待审核中':
            print('第{}个测试用例：主账户{}个人资讯填写完成等待审核'.format(self.subp+1,data['主账户']))
        else:
            print('个人资讯填写失败')

if __name__=='__main__':
    #生成测试报告
    suit=unittest.defaultTestLoader.discover('./',pattern='KYC_vfcation.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='KYC验证测试报告',description='不同证件签发国KYC验证通过',report_dir='all_case_report')