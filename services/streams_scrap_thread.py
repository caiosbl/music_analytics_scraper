import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

SPOTIFY_STREAMS_COUNT_XPATH = '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[1]/div[5]/div/span[4]'

class StreamPlaysScrapThread(threading.Thread):
    def __init__(self, track, pool, implicitly_wait=5):
        threading.Thread.__init__(self)
        self.track = track
        self.pool = pool
        self.implicitly_wait = implicitly_wait

    def run(self):
        driver = self.pool.get_driver()
        try:
            driver.get(self.track.url)
            WebDriverWait(driver, self.implicitly_wait).until(
                lambda x: x.find_element(By.XPATH, SPOTIFY_STREAMS_COUNT_XPATH)
            )
            stream_element = driver.find_element(By.XPATH, SPOTIFY_STREAMS_COUNT_XPATH)
            streams_count = int(stream_element.text.replace('.', '').replace(',', ''))
            self.track.streams_count = streams_count
        except Exception as e:
            print(f"Error getting streams for track {self.track.id}: {e}")
            raise FailToGetStreamsException()
        finally:
           self.pool.release_driver(driver)

class FailToGetStreamsException(Exception):
    pass