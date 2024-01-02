from queue import Queue
from selenium import webdriver

class WebDriverPool:
    def __init__(self, size, implicitly_wait=3):
        self.available = Queue()
        for _ in range(size):
            driver = webdriver.Chrome(
                implicitly_wait=implicitly_wait
            )
            self.available.put(driver)

    def get_driver(self):
        return self.available.get()

    def release_driver(self, driver):
        self.available.put(driver)

