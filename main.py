import queue
import threading
import time
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
import kivy

from pySmartDL import SmartDL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from kivy.app import App
from kivy.uix.label import Label
from selenium.webdriver.chrome.options import Options

save_loc = "E:/KSD/"


class DownloadManager:
    def __init__(self):
        self.q = queue.Queue(maxsize=20)
        self.is_serving = False

    def add(self, dl_job):
        self.q.put(dl_job)

    def serve(self):
        if not self.is_serving:
            dl_job = self.q.get()
            print("Starting")
            self.is_serving = True
            # print(dl_job[3])
            # time.sleep(2)
            try:
                obj = SmartDL(dl_job[3], dest=dl_job[-1])
                obj.start(blocking=False)
                # path = obj.get_dest()
                while not obj.isFinished():
                    print("Speed: %s" % obj.get_speed(human=True))
                    print("Progress: %s" % (obj.get_progress() * 100))
                print("ENDED")
                self.is_serving = False
            except Exception:
                print("Error")
                # errors = obj.get_errors()
                # for error in errors:
                #     print(str(type(error)))
                self.is_serving = False
                # self.q.put(dl_job)

        #else:
           # print("currently serving, waiting")

            # if obj.isSuccessful():
            #     print("DOWNLOADED SUCCESSFULLY!!")
            # else:
            #     print("Download failed with the following exceptions:")
            #     for e in obj.get_errors():
            #         print(e)


class DownloadManagerThread(threading.Thread):
    def __int__(self):
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            if not download_manager.q.empty():
                download_manager.serve()
            else:
                #print("Download Manager: Empty Queue")
                time.sleep(1)


class MyApp(App):
    def build(self):
        return Label(text='Hello World')


def scrape_urls(url):
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("C:/chromedriver.exe") # , options=chrome_options
    driver.get(url)

    print("Extracting...")

    try:
        wait = WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div[3]/div/div/ul/li/a"), "Home")
        )
    except NoSuchElementException:
        print("not Found")

    episodes = driver.find_elements_by_xpath("/html/body/div/div[4]/div/div[2]/div[2]/div[2]/table/tbody/tr")[2:]
    episode_list = []

    for episode in reversed(episodes):
        elem = episode.find_element_by_tag_name("td").find_element_by_tag_name("a")
        ep = [elem.text, elem.get_attribute("href")]
        episode_list.append(ep)

    for episode in episode_list:
        driver.get(episode[1] + "&s=rapidvideo")

        path = driver.find_element_by_id("divMyVideo").find_element_by_tag_name("iframe").get_attribute("src")

        index = path.rfind('/', 0, len(path) - 1) + 1
        path = "https://www.rapidvideo.com/d/" + path[index:]
        episode.append(path)

        driver.get(path)
        qualities = driver.find_element_by_class_name("hero-body").find_elements_by_class_name("title")[
            1].find_elements_by_tag_name("a")

        # 480, 720, 1080
        quality_links = ["", "", ""]

        for quality in qualities:
            if quality.text == "Download 480p":
                quality_links[0] = quality.get_attribute("href")
            elif quality.text == "Download 720p":
                quality_links[1] = quality.get_attribute("href")
            elif quality.text == "Download 1080p":
                quality_links[2] = quality.get_attribute("href")
            else:
                print("UNKNOWN QUALITY: " + quality.text)

        # FOR HIGHEST QUALITY DOWNLOAD
        quality_links.reverse()
        episode.append(quality_links)

        episode.append(save_loc + str(episode[0]).replace(' ', '_') + ".mp4")

        print(episode)
    driver.close()
    return episode_list


if __name__ == "__main__":
    download_manager = DownloadManager()
    dm_thread = DownloadManagerThread()
    dm_thread.start()

    data = scrape_urls("https://kissanime.ru/Anime/Radiant")

    for item in data:
        # print(item)
        download_manager.add(item)

    # MyApp().run()
    # print("Done")
