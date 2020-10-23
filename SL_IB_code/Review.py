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

@ddt.ddt
class review(unittest.TestCase,basepage):
    """bos初审通过"""
    def setUp(self):
        self.dr=webdriver.Chrome()
        #实例化父类
        self.pub = basepage(self.dr)
        self.dr.get('https://at-bos-frontend-uat.atfxdev.com/login')
        time.sleep(1)

    def tearDown(self):
        self.dr.close()
        self.dr.quit()

    @ddt.data(*testdata)
    def test_review(self,data):
        #获取测试数据的下标
        subp = testdata.index(data)
        print('当前测试数据：{}'.format(data['主账户']))
        #登录bos
        self.login_bos('tyler','Tl123456')
        #审核初审及创建交易账户
        self.review_success(data['主账户'])
        print('第{}个账户修改ibcode成功，主账户：{}'.format(subp+1,data['主账户'],))

if __name__=='__main__':
    # 生成测试报告
    suit=unittest.defaultTestLoader.discover('./',pattern='*view.py',top_level_dir=None)
    BeautifulReport(suit).report(filename='初审通过测试报告',description='用例执行情况',report_dir='all_case_report')