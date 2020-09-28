#导包
from selenium import webdriver
from country_list import exceldata
import ddt
import unittest
from BeautifulReport import BeautifulReport
from public import basepage

#提取测试文档数据
e=exceldata()
rows=e.openexcel(r'E:\test\country.xlsx','Sheet1') #测试文档的路径，sheet名,并获取总行数
testdata=e.dict_data()

#创建类，继承unittest.TestCase类：
@ddt.ddt #数据驱动
class creat_account(unittest.TestCase,basepage):
    """2.0会员中心注册流程,根据国家列表注册对应的证件签发国账户"""

    def setUp(self):#预置条件,注册销售/代理，更改链接即可
        self.dr = webdriver.Chrome()
        #实例化父类对象，继承初始化函数属性
        self.pub = basepage(self.dr)

    def tearDown(self):#环境恢复
        self.dr.quit()

    #填写表单
    @ddt.data(*testdata)
    def test_fill_form(self,data):
        print('当前测试数据:国家：{}；三字码：{}；邮箱：{}；账户类型：{}'.format(data['国家'],data['三字码'],data['邮箱'],data['账号类型']))
        if self.is_uk(data['国家']):
            self.dr.close()
        else:
            #访问url
            self.get_url(data['账号类型'])
            # 获取每组测试数据的下标
            self.subp = testdata.index(data)
            #填写注册页表单,姓名及密码可自己编辑
            self.register_form(data['三字码'],data['国家'],data['邮箱'],'TYLERTEST','Tl123456')
            #点击登录后弹窗
            self.login_top()
            # 保存测试数据到本地文档
            self.saveaccount(r'E:\test\account_number.xlsx',data['国家'], 'A', self.subp + 2)
            self.saveaccount(r'E:\test\account_number.xlsx',data['邮箱'], 'B', self.subp + 2)
            self.saveaccount(r'E:\test\account_number.xlsx', data['三字码'], 'H', self.subp + 2)
            # 获取主账号,并保存至本地文档
            textid = self.page_text('.user-name-font') + ' '
            self.id = textid[4:-1]
            self.saveaccount(r'E:\test\account_number.xlsx',self.id, 'C', self.subp + 2)
            #ib账户点击ib返佣表格
            if self.id[0:2]=='10':
                self.ib_table()
            else:
                pass
            print('第{}个测试数据注册成功，主账户：{}'.format(self.subp + 1, self.id))

if __name__=='__main__':
    #生成测试报告
    suit=unittest.defaultTestLoader.discover('./',pattern='*portal_register.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='2.0会员中心注册测试报告',description='不同证件签发国注册账户',report_dir='all_case_report')