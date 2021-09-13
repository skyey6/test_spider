from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.firefox.options import Options
import json

site_name = "成都市经济和信息化局"
basic_url = 'http://cdjx.chengdu.gov.cn/'
title, date, url = '', '', ''
my_list = []

if __name__ == '__main__':
    # options用来控制浏览器以无界面模式打开
    options = Options()
    # options.headless = True
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Firefox(options=options)
    browser.implicitly_wait(3)  # 如果没有找到节点，等待3秒
    try:
        browser.get(basic_url)

        # 根据xpath获取 通知公告 中每个节点
        # lis为全部节点组成的列表
        lis = browser.find_elements_by_xpath(f'/html/body/div[5]/div[2]/div[1]/div[2]/div[2]/ul[1]/li')
        # print(lis)
        # print(len(lis))

        for li in lis:
            title = li.find_element_by_tag_name('a').get_attribute('title')
            url = li.find_element_by_tag_name('a').get_attribute('href')
            date = li.find_element_by_tag_name('span').text
            my_list.append({'title': title, 'url': url, 'date': date})

        # 写入txt文件
        with open(f'../results/{site_name}.txt', 'w', encoding='utf-8') as f:
            for item in my_list:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

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
