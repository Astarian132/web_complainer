from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import dotenv
import time
TWITTER_EMAIL = dotenv.dotenv_values('python.env').get("twitter_email")
TWITTER_USER = dotenv.dotenv_values('python.env').get("twitter_user")
TWITTER_PASSWORD = dotenv.dotenv_values('python.env').get('twitter_password')
EDGE_WEBDRIVER_PATH = dotenv.dotenv_values(
    'python.env').get('edge_webdriver_path')
CONTRACTED_MIN_DOWN = 150
CONTRACTED_MIN_UP = 20
profile = webdriver.EdgeOptions()
profile.add_argument("start-maximized")
profile.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])


class InternetSpeedTwitterBot():
    def __init__(self) -> None:
        self.driver = webdriver.Edge(
            executable_path=EDGE_WEBDRIVER_PATH, options=profile)
        self.down = 0
        self.up = 0
        self.latency = 9999

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net")
        try:
            accept_button = self.driver.find_element(
                By.ID, 'onetrust-accept-btn-handler')
            accept_button.click()
        finally:
            start_button = self.driver.find_element(
                By.CLASS_NAME, 'start-text')
            start_button.click()
            if WebDriverWait(self.driver, 100).until(
                    EC.url_contains("https://www.speedtest.net/result/")):
                self.up = self.driver.find_element(
                    By.CLASS_NAME, "upload-speed").text
                self.down = self.driver.find_element(
                    By.CLASS_NAME, "download-speed").text
                self.latency = self.driver.find_element(
                    By.CLASS_NAME, "ping-speed").text
            print(f"Download speed:{self.down}Mb/s")
            print(f"Upload speed: {self.up}Mb/s")
            print(f"Ping: {self.latency}ms")

    def tweet_results(self):
        self.driver.get("https://twitter.com/")
        login = self.driver.find_element(
            By.XPATH, '//*[@id="layers"]/div/div[1]/div/div/div/div[2]/div[2]/div/div/div[1]/a')
        login.click()
        time.sleep(3)
        credentials = self.driver.find_element(
            By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
        credentials.click()
        credentials.send_keys(TWITTER_USER)
        credentials.send_keys(Keys.ENTER)
        time.sleep(2)
        password_field = self.driver.find_element(
            By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        password_field.send_keys(TWITTER_PASSWORD)
        password_field.send_keys(Keys.ENTER)
        time.sleep(6)
        print(self.driver.current_url)
        self.driver.current_url
        tweet_details = self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div')
        tweet_details.click()
        tweet_details.send_keys(
            f"Hello webprovider, my current download speed is {self.down}Mb/s, upload speed {self.up}Mb/s with ping {self.latency}ms.")
        send_tweet = self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div/div/span/span')
        send_tweet.click()
        time.sleep(5)
        self.driver.quit()


if __name__ == "__main__":
    internet_bot = InternetSpeedTwitterBot()
    internet_bot.get_internet_speed()
    if internet_bot.down < CONTRACTED_MIN_DOWN or internet_bot.up < CONTRACTED_MIN_UP:
        internet_bot.tweet_results()
