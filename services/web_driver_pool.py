from queue import Queue
from selenium import webdriver

class WebDriverPool:
    def __init__(
        self,
        size,
        webdriver_path,
        webdriver_chromium_path,
    ):
        self.available = Queue()
        for _ in range(size):
            driver = self.get_webdriver(webdriver_chromium_path, webdriver_path)
            self.available.put(driver)


    def get_webdriver(self, webdriver_chromium_path, webdriver_path):
        webdriver_option = webdriver.ChromeOptions()
        webdriver_option.add_argument('--headless')
        webdriver_option.add_argument('--no-sandbox')
        webdriver_option.add_argument("--disable-gpu")
        webdriver_option.add_argument("window-size=1200x600")
        webdriver_option.binary_location = webdriver_chromium_path
        
        return webdriver.Chrome(
            options=webdriver_option,
        )

    def get_driver(self):
        return self.available.get()

    def release_driver(self, driver):
        self.available.put(driver)

