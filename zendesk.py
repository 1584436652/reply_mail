import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mail import Mail


class ZendeskMail(Mail):
    def __init__(self):
        super(ZendeskMail, self).__init__(),
        self.options = Options()
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-javascript')
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(executable_path="./谷歌驱动/chromedriver.exe", options=self.options)
        self.wait = WebDriverWait(self.driver, 5)
        self.filters_url = 'https://anke.zendesk.com/agent/filters'
        self.login_url = 'https://anke.zendesk.com/auth/v2/login/'
        self.driver.get(self.login_url)

    def zendesk_login(self, em="TEST"):
        # 邮箱
        self.wait.until(
            EC.presence_of_element_located((By.ID, "user_email"))).send_keys("nilala520@gmail.com")
        time.sleep(2)
        # 密码
        self.wait.until(
            EC.presence_of_element_located((By.ID, "user_password"))).send_keys("Anke168168")
        self.wait.until(
            EC.element_to_be_clickable((By.ID, 'sign-in-submit-button'))).click()
        time.sleep(3)
        # 发邮件页面
        self.driver.get(self.filters_url)
        time.sleep(4)
        # 添加
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="wrapper"]//span[@class="LRae LRaf"]'))).click()
        time.sleep(1)
        self.wait.until(
            EC.presence_of_element_located((By.ID, "mn_1"))).send_keys(em)
        # self.wait.until(
        #     EC.element_to_be_clickable((By.ID, 'downshift-17-input'))).clicl()
        # time.sleep(1)
        # self.wait.until(
        #     EC.presence_of_element_located((By.ID, 'downshift-17-input'))).send_keys("DONG")


if __name__ == '__main__':
    zen = ZendeskMail()
    zen.zendesk_login()
