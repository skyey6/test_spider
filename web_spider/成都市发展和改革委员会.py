from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.firefox.options import Options
import json

site_name = "成都市发展和改革委员会"
basic_url = "http://cddrc.chengdu.gov.cn/cdfgw/c120588/jksj_list.shtml?classId=070305020301&pageNum="
title, date, url = '', '', ''
my_list = []

if __name__ == '__main__':
    # 设置浏览器以无界面模式打开
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Firefox(options=options)
    browser.implicitly_wait(3)

    try:
        # browser.get(basic_url)
        # element1 = browser.find_element_by_css_selector(".pagination-last")
        # pageNum = element1.find_element_by_xpath("span[3]").text
        # pageNum = pageNum.split(' ')[1]
        # print(pageNum)
        # for page in range(1, pageNum+1):  # 爬取全部页
        for page in range(1, 10+1):  # 爬取前10页
            site_url = basic_url + str(page)
            browser.get(site_url)
            lis = browser.find_elements_by_css_selector('#ajax_list li')
            for li in lis:
                title = li.find_element_by_tag_name('a').get_attribute('title')
                url = li.find_element_by_tag_name('a').get_attribute('href')
                date = li.find_element_by_xpath("a/span[2]").text
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

