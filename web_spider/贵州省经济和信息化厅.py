from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.firefox.options import Options
import json

site_name = "贵州省经济和信息化厅"
basic_url = "http://gxt.guizhou.gov.cn/"
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
        lis = browser.find_elements_by_xpath('//div[@class="zcwj-box mt5"]/div/ul/li')
        for li in lis:
            document_type = li.find_element_by_xpath('a/i').text[1:-1]
            title = li.find_element_by_tag_name('a').get_attribute('title')
            url = li.find_element_by_tag_name('a').get_attribute('href')
            date = li.find_element_by_tag_name('span').text
            # print(date)
            my_list.append({'type': document_type, 'title': title, 'url': url, 'date': date})

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
