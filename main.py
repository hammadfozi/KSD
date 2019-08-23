import queue
import threading
import time

from pySmartDL import SmartDL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


class DownloadManager:
    def __init__(self):
        self.q = queue.Queue(maxsize=20)

    def add(self, dl_job):
        self.q.put(dl_job)

    def serve(self):
        dl_job = self.q.get()
        print("Starting")

        obj = SmartDL(dl_job["url"], dest=dl_job["dest"])
        obj.start(blocking=False)
        # path = obj.get_dest()
        while not obj.isFinished():
            print("Speed: %s" % obj.get_speed(human=True))
            print("Progress: %s" % (obj.get_progress() * 100))

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
                print("Download Manager: Empty Queue")
                time.sleep(1)


if __name__ == "__main__":
    # download_manager = DownloadManager()
    # dm_thread = DownloadManagerThread()
    # dm_thread.start()
    #
    # dl1 = {
    #     "url": "https://www79.playercdn.net/p-dl/1/eG6Wu8AuddMtZpR6PAlvQA/1566566286/190822/086G686J2D1XPTX5SCINB.mp4?name=FateStayNightHeavensFeelIILostButterflyBDRip1920x1080x264FLAC-rh-332.mp4-1080.mp4",
    #     "dest": "D:/"
    # }
    #
    # download_manager.add(dl1)
    #
    # print("Ended")

    driver = webdriver.Chrome("C:/chromedriver.exe")
    driver.get("https://kissanime.ru/Anime/Dr-Stone")

    #episodes = driver.find_element_by_class_name("listing").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
    wait = WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[3]/div/div/ul/li/a"))
      )

    print("YES")
    print(driver.find_element_by_xpath("/html/body/div/div[4]/div/div[2]/div[2]/div[2]/table").text)
    # episodes = driver.find_element_by_xpath("/html/body/div/div[4]/div/div[3]/div[2]/div[2]/table")
    #
    # #print(episodes.text)
    #
    # for episode in episodes:
    #    print(episode.text)

