import spotipy
import tqdm
import chromedriver_autoinstaller
import threading

from queue import Queue
from spotipy.oauth2 import SpotifyClientCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

class StreamPlaysScrapThread(threading.Thread):
    def __init__(self, track, pool):
        threading.Thread.__init__(self)
        self.track = track
        self.pool = pool
        self.streams_count = None

    def run(self):
        driver = self.pool.get_driver()
        try:
            driver.get(self.track["track_url"])
            WebDriverWait(driver, 10).until(
                lambda x: x.find_element(By.XPATH, SPOTIFY_STREAMS_COUNT_XPATH)
            )
            stream_element = driver.find_element(By.XPATH, SPOTIFY_STREAMS_COUNT_XPATH)
            self.streams_count = int(stream_element.text.replace('.', '').replace(',', ''))
        except Exception as e:
            print(f"Error getting streams for track {self.track['id']}: {e}")
        finally:
           self.pool.release_driver(driver)