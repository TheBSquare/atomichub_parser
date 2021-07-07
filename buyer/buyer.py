import threading

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import time

from selenium.webdriver.common.keys import Keys


class Buyer:
    def __init__(self):
        options = Options()
        options.headless = False
        options.add_argument(r"--user-data-dir=C:\Users\thede\AppData\Local\Google\Chrome\User Data")
        options.add_argument(r'--profile-directory=Default')
        self.driver = Chrome(
            executable_path=r"D:\projects\nfts\chromedriver.exe",
            options=options
        )
        self.driver.get("https://wax.bloks.io/")

        time.sleep(2)

        input1 = self.driver.find_element_by_css_selector("input.search")
        input1.send_keys("atomicmarket")
        input1.send_keys(Keys.ENTER)

        time.sleep(3)

        button1 = self.driver.find_element_by_css_selector("div.eight:nth-child(2)")
        button1.click()

        time.sleep(2)

        button2 = self.driver.find_element_by_css_selector("div.top:nth-child(3) > div:nth-child(2)")
        self.driver.execute_script("arguments[0].click()", button2)

        time.sleep(2)

        button3 = self.driver.find_element_by_css_selector("span.ui:nth-child(29)")
        self.driver.execute_script("arguments[0].click()", button3)

        time.sleep(2)

        button4 = self.driver.find_element_by_css_selector(
            "#header-grid > div:nth-child(1) > div > div > div > div.ui.floating.dropdown > div"
        )
        self.driver.execute_script("arguments[0].click()", button4)

        time.sleep(2)

        button5 = self.driver.find_element_by_css_selector(
            "#header-grid > div:nth-child(3) > div > div > div.v--modal-box.v--modal > div > "
            "div.buttons-container > div > div:nth-child(1) > div"
        )
        self.driver.execute_script("arguments[0].click()", button5)

        time.sleep(5)

        self.buyer_b = self.driver.find_element_by_css_selector(
            "div.unstackable:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)"
        ).send_keys("tmteo.wam")

        self.sale_id_b = self.driver.find_element_by_css_selector(
            "div.sixteen:nth-child(2) > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)"
        )

        self.delphi_b = self.driver.find_element_by_css_selector(
            "div.sixteen:nth-child(3) > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)"
        ).send_keys('0')

        self.taker = self.driver.find_element_by_css_selector(
            "div.sixteen:nth-child(4) > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)"
        ).send_keys('""')

        self.submit_b = self.driver.find_element_by_css_selector("#push-transaction-btn")

    def buy(self, sale_id):
        self.sale_id_b.send_keys(sale_id),
        self.driver.execute_script("arguments[0].click()", self.submit_b)


if __name__ == '__main__':
    t = Buyer()
    ti = time.time()
    t.buy('23408798')
    print(time.time()-ti)
