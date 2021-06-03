from selenium import webdriver
import json
import time
import os


class SeleniumCrawler:
    def __init__(self, cfg) -> None:
        self.cookie_file = cfg.SELENIUM.COOKIE_FILE
        self.safe_delay = cfg.SELENIUM.SAFE_DELAY
        self.driver = self.launch(cfg.SELENIUM.CHROMEDRIVER_PATH)

    def launch(self, driver_path) -> webdriver:
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")
        driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
        return driver

    def delay(self) -> None:
        time.sleep(self.safe_delay)

    def save_cookies(self):
        cookies = self.driver.get_cookies()
        with open(self.cookie_file, "w") as f:
            json.dump(cookies, f, indent=4)

    def load_cookies(self, domain):
        self.driver.get(domain)

        if not os.path.exists(self.cookie_file):
            return -1

        with open(self.cookie_file, "r") as f:
                cookies = json.load(f)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        return 0
