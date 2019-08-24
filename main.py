import queue
import threading
import time

from pySmartDL import SmartDL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

save_loc = "G:/KSD/"

class DownloadManager:
    def __init__(self):
        self.q = queue.Queue(maxsize=20)
        self.is_serving = False

    def add(self, dl_job):
        self.q.put(dl_job)

    def serve(self):
        if not self.is_serving:
            self.is_serving = True
            dl_job = self.q.get()
            print("Starting")

            obj = SmartDL(dl_job[3][0], dest=dl_job[-1])
            obj.start(blocking=False)
            # path = obj.get_dest()
            while not obj.isFinished():
                print("Speed: %s" % obj.get_speed(human=True))
                print("Progress: %s" % (obj.get_progress() * 100))

            self.is_serving = False
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
    download_manager = DownloadManager()
    dm_thread = DownloadManagerThread()
    dm_thread.start()

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

    print("Extracting...")
    #episodes = driver.find_element_by_class_name("listing").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
    # wait = WebDriverWait(driver, 10).until(
    #      EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[3]/div/div/ul/li/a"))
    #   )

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
        #print(elem.text)
        #print(elem.get_attribute("href"))
        ep = [elem.text, elem.get_attribute("href")]
        episode_list.append(ep)

    for episode in episode_list:
        # print(episode)
        driver.get(episode[1] + "&s=rapidvideo")

        path = driver.find_element_by_xpath("/html/body/div/div[4]/div/div/div/div[13]/div[2]/div/iframe").get_attribute("src")
        index = path.rfind('/', 0, len(path)-1) + 1
        path = "https://www.rapidvideo.com/d/" + path[index:]
        episode.append(path)

        driver.get(path)
        #qualities = driver.find_elements_by_xpath("/html/body/div/section/section/div/div/p[2]/a")
        qualities = driver.find_element_by_class_name("hero-body").find_elements_by_class_name("title")[1].find_elements_by_tag_name("a")

        # 480, 720, 1080

        quality_links = ["", "", ""]

        for quality in qualities:
            # print(quality.text)
            # print(quality.get_attribute("href"))
            if quality.text == "Download 480p":
                quality_links[0] = quality.get_attribute("href")
            elif quality.text == "Download 720p":
                quality_links[1] = quality.get_attribute("href")
            elif quality.text == "Download 1080p":
                quality_links[2] = quality.get_attribute("href")
            else:
                print("UNKNOWN QUALITY: " + quality.text)

        episode.append(quality_links)

        episode.append(save_loc + str(episode[0]).replace(' ', '_') + ".mp4")

        print(episode)
        download_manager.add(episode)
    print("Done")
    # .get_attribute("src")

    # try:
    #     wait = WebDriverWait(driver, 10).until(
    #      EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div[3]/div/div/ul/li/a"), "Home")
    #     )
    # except NoSuchElementException:
    #     print("not Found")
    #
    # driver.find_element_by_xpath("/html/body/div/div[4]/div/div[2]/form/div[3]/")




