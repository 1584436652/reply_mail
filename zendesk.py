import time
from retry import retry
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mail import Mail
from zendesk_config import USER_MAIL, USER_PASSWORD


class ZendeskMail(Mail):

    def __init__(self):
        super(ZendeskMail, self).__init__(),
        self.options = Options()
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-javascript')
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(executable_path="./谷歌驱动/chromedriver.exe", options=self.options)
        self.wait = WebDriverWait(self.driver, 4)
        self.filters_url = 'https://anke.zendesk.com/agent/tickets/new/1'
        self.login_url = 'https://anke.zendesk.com/auth/v2/login/'
        self.driver.get(self.login_url)

    def zendesk_login(self):
        """
        模拟登录
        :return:
        """
        # 邮箱
        self.wait.until(
            EC.presence_of_element_located((By.ID, "user_email"))).send_keys(USER_MAIL)
        time.sleep(1)
        # 密码
        self.wait.until(
            EC.presence_of_element_located((By.ID, "user_password"))).send_keys(USER_PASSWORD)
        self.wait.until(
            EC.element_to_be_clickable((By.ID, 'sign-in-submit-button'))).click()
        time.sleep(2)

    @retry(delay=3)
    def zendesk_operate(self, **kwargs):
        """
        具体操作
        :return:
        """
        try:
            # 发邮件页面
            self.driver.get(self.filters_url)
            time.sleep(4)
            # 添加
            self.wait.until(
                EC.presence_of_element_located((By.ID, "mn_1"))).send_keys(kwargs["contact_email"])
            time.sleep(1.5)
            # 要发送的信息
            self.wait.until(
                EC.presence_of_element_located((By.XPATH,
                                                '//div[@class="ck-blurred ck ck-content ck-editor__editable ck-rounded-corners ck-editor__editable_inline"]'))).send_keys(kwargs["message"])
            time.sleep(2.5)
            # svg下拉
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            '//div[@id="main_panes"]//div[@class="LRbr"]//div[@data-garden-id="dropdowns.faux_input"]//*[name()="svg"]'))).click()
            time.sleep(2)
            # 输入分组
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="downshift-5-input"]'))).send_keys("冬笋")
            time.sleep(1)
            # 点击选择的分组
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="downshift-5-item-0"]/div'))).click()
            time.sleep(1)
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="downshift-5-item-1"]/div'))).click()
            time.sleep(1)
            # 标题
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@id="main_panes"]//input[@data-garden-id="forms.input"]'))).send_keys(kwargs["title"])
            time.sleep(1)
            # 提交的svg
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            '//div[@id="main_panes"]//div[@class="LRb LRc"]//button[@data-garden-id="buttons.icon_button"]//*[name()="svg"]'))).click()
            time.sleep(0.5)
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            '//div[@id="main_panes"]//div[@class="LRb LRc"]/div[@data-garden-id="chrome.footer_item"][2]//ul/li[3]'))).click()
            time.sleep(3)
        # except UnexpectedAlertPresentException:
        #     time.sleep(2)
        except TimeoutException as e:
            print(f'{kwargs["title"]}有元素没查找到，继续当前信息发送)')
            raise e

    def add_information(self):
        for item in self.read_table():
            title = item[0]
            contact_email = item[3]
            message = item[6]
            yield {
                "title": title,
                "contact_email": contact_email,
                "message": message
            }

    def run(self):
        for me in self.add_information():
            self.zendesk_operate(**me)


if __name__ == '__main__':
    zen = ZendeskMail()
    zen.zendesk_login()
    zen.run()
