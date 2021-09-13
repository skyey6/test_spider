from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.firefox.options import Options
import json

site_name = "四川省经济和信息化厅"
basic_url = "https://jxt.sc.gov.cn/"
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
        hover = browser.find_element_by_xpath("//div[5]/div[4]/div[1]/div/ul/li[2]/a")
        hover.click()   # 选中“文件发布”
        element = browser.find_element_by_css_selector("div #panel-20002")
        lis = element.find_elements_by_xpath("ul/li")
        for li in lis:
            title = li.find_element_by_tag_name('a').get_attribute('title')
            url = li.find_element_by_tag_name('a').get_attribute('href')
            date = li.find_element_by_tag_name('span').text
            # print(date)
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