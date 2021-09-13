from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.firefox.options import Options
import json

site_name = "四川省发展和改革委员会"
basic_url = "http://fgw.sc.gov.cn/"
title, date, url = '', '', ''
my_list = []

if __name__ == '__main__':
    # 设置浏览器以无界面模式打开
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Firefox(options=options)
    browser.implicitly_wait(3)  # 如果没有找到节点，等待3秒
    try:
        browser.get(basic_url)
        hover = browser.find_element_by_xpath("//div[2]/div/div/div[1]/div[1]/div[2]/div[1]/ul/li[2]/a")
        hover.click()  # 选中“通知公告”
        lis = browser.find_elements_by_xpath('//div[2]/div[1]/div[@class="lmqh_div2 gayw3"]/ul[2]/li')
        # print(lis)
        for li in lis:
            title = li.find_element_by_tag_name('a').get_attribute('title')
            url = li.find_element_by_tag_name('a').get_attribute('href')
            date = li.find_element_by_tag_name('span').text
            my_list.append({'title': title, 'url': url, 'date': date})

        # 写入json文件
        with open(f'../results/{site_name}.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(my_list, ensure_ascii=False, indent=2))

        print('数据爬取结束...')

    except TimeoutException as e:
        print(e.msg)
    except NoSuchElementException as e:
        print(e.msg)
    finally:
        browser.close()
