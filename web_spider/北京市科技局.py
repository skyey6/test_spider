from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.firefox.options import Options
import json

site_name = "北京市科技局"
basic_url = "http://kw.beijing.gov.cn/col/col736/index.html###"
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
        next_page_bottom = browser.find_element_by_xpath("//div[6]/div[2]/div[2]/div/div/a[1]")
        for page in range(1, 5+1):   # 爬取前5页
            lis = browser.find_elements_by_xpath("//div[6]/div[2]/div[2]/div/ul/li")
            for li in lis:
                title = li.find_element_by_tag_name('a').text
                url = li.find_element_by_tag_name('a').get_attribute('href')
                date = li.find_element_by_tag_name('span').text
                # print(date)
                my_list.append({'title': title, 'url': url, 'date': date})
            next_page_bottom.click()
            # 每次翻页后重新获取翻页按钮，避免 StaleElementReferenceException
            next_page_bottom = browser.find_element_by_xpath("//div[6]/div[2]/div[2]/div/div/a[3]")

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
