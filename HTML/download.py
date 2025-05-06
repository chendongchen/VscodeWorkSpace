import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 设置浏览器驱动（确保你已经安装了相应的浏览器驱动，如 chromedriver）
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 目标URL
url = 'https://zjdph.8nary.com/forum-155-1.html'

# 打开网页
driver.get(url)

# 等待页面加载完成
driver.implicitly_wait(10)  # 等待10秒

# 查找所有链接
links = driver.find_elements(By.TAG_NAME, 'a')

# 输出所有链接
for link in links:
    href = link.get_attribute('href')
    if href:
        print(href)

# 关闭浏览器
driver.quit()