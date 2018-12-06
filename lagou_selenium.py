from selenium import webdriver
from lxml import html
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ES

class LagouSpider():

    def __init__(self):
        self.path = 'E:\leidownload\chromedriver_win32\chromedriver.exe'
        self.driver=webdriver.Chrome(executable_path=self.path)
        self.url='https://www.zhipin.com/job_detail/?query=python&scity=101020100&industry=&position='
        self.hiring=[]

    def detail_sourse(self,url):
        """
        获取详情页面的资源
        :param url:
        :return:
        """
        self.driver.execute_script("window.open('%s')"%url)
        self.driver.switch_to.window(self.driver.window_handles[1])
        detail_sourse=self.driver.page_source
        detail_sourse=html.etree.HTML(detail_sourse)
        self.get_detail_msg(detail_sourse)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def get_detail_msg(self,detail_sourse):
        """
        获取页面数据
        :return:
        """
        company=detail_sourse.xpath("//a[@ka='job-detail-company']/text()")[0]
        position=detail_sourse.xpath('//div[@class="name"]//h1/text()')[0]
        desc=detail_sourse.xpath('//div[@class="detail-content"]/div[1]/div/text()')[0].strip()
        # team=detail_sourse.xpath('//div[@class="detail-content"]/div[2]/div[@class="text"]/text()')[0].strip()
        salary=detail_sourse.xpath('//div[@class="name"]/span[@class="badge"]/text()')[0].strip()
        data={
            'company':company,
            'position':position,
            'desc':desc,
            # 'team':team
            'salary':salary
        }
        self.hiring.append(data)
        print(data)

    def get_url_list(self,sourse):
        """
        获取下一页地址的url
        :return:url
        """
        url_list=sourse.xpath("//div[@class='job-list']/ul//li")
        print(url_list)
        for each_url in url_list:
            detail_url=each_url.xpath('.//h3/a/@href')[0]
            detail_url='http://www.zhipin.com'+detail_url
            time.sleep(2)
            self.detail_sourse(detail_url)

    def run(self):
        self.driver.get(self.url)
        while True:
            sourse=html.etree.HTML(self.driver.page_source)
            self.get_url_list(sourse)
            next_page=self.driver.find_element_by_class_name('next')
            if 'disabled' in next_page.get_attribute('class'):
                break
            else:
                time.sleep(4)
                next_page.click()

if __name__ == "__main__":
    lagou=LagouSpider()
    lagou.run()
    print(lagou.hiring)
