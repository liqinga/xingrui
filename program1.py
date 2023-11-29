# -*- codeing = utf-8 -*-
# @Time : 2023/11/29 3:21 下午
# @Author : Li Qing
# @File : program1.py
# @Software : PyCharm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import csv
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

def perform_web_scraping(url):
    # 使用Selenium模拟浏览器行为
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        # 使用显式等待确保元素加载完毕
        element_present = EC.presence_of_element_located((By.ID, 'Bond_Type_select'))
        WebDriverWait(driver, 10).until(element_present)

        # 找到id为Bond_Type_select的select标签
        bond_type_select = Select(driver.find_element(By.ID, "Bond_Type_select"))
        # 将select标签的值设置为10001
        bond_type_select.select_by_value('100001')

        # 找到id为Issue_Year_select的select标签
        issue_year_select = Select(driver.find_element(By.ID, "Issue_Year_select"))
        # 将Issue_Year_select的值设置为2023
        issue_year_select.select_by_value('2023')

        # 等待一段时间，确保页面有足够时间响应
        time.sleep(2)

        # 找到search按钮并点击
        search_button = driver.find_element(By.XPATH, '//a[@class="san-btn san-btn-primary" and text()="Search"]')
        search_button.click()

        # 等待一段时间，确保页面有足够时间响应
        time.sleep(5)

        # 获取搜索结果的HTML内容
        html_content = driver.page_source

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 找到class为"san-sheet-alternating"的table标签
        table = soup.find('table', {'class': 'san-sheet-alternating'})

        # 提取表格数据
        table_data = []

        if table:
            headers = [header.text.strip() for header in table.select('thead td')]
            rows = table.select('tbody tr')
            for row in rows:
                row_data = [cell.text.strip() for cell in row.find_all('td')]
                table_data.append(row_data)

        # 写入CSV文件
        if headers and table_data:
            with open('program.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(headers)
                csv_writer.writerows(table_data)
            print("表格数据已写入 program.csv 文件,第一次写入")
        else:
            print("未找到表格数据")

        while True:
            # 提取表格数据
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find('table', {'class': 'san-sheet-alternating'})

            # 提取表格数据
            rows = table.select('tbody tr')
            table_data = [[cell.text.strip() for cell in row.find_all('td')] for row in rows]

            # 追加到CSV文件
            if table_data:
                with open('program.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerows(table_data)
            print(table_data)

            # 查找并点击"Next"按钮
            try:
                next_button = driver.find_element(By.XPATH,
                                                  '//a[contains(text(), "Next")]')
                next_button.click()
                # 等待新页面加载完成
                WebDriverWait(driver, 10).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                time.sleep(5)  # 根据实际情况调整等待时间
            except StaleElementReferenceException:
                print("捕获到 StaleElementReferenceException 异常，尝试等待重新加载。")
                time.sleep(2)
            except NoSuchElementException:
                print("下一个按钮不再可点击。退出循环。")
                break

    finally:
        # 关闭浏览器
        driver.quit()

if __name__ == "__main__":
    url = "https://iftp.chinamoney.com.cn/english/bdInfo/"
    perform_web_scraping(url)