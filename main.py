import queue
import threading
import time

from pySmartDL import SmartDL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QLabel, QProgressBar, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import pyqtSignal

save_loc = "G:/KSD/"
episode_list = [['Babylon Episode 001', 'https://kissanime.ru/Anime/Babylon/Episode-001?id=162738', 'https://www.rapidvideo.com/d/G7PDRNJHUS', ['https://www278.playercdn.net/p-dl/2/dIBvv0pVJ6lVLpW0P4oPEg/1570500280/191007/106G7PDUDLM2T0IOMVQM5.mp4?name=HorribleSubsBabylon011080pr527.x.mp4-rh-108.mp4-1080.mp4', 'https://www370.playercdn.net/p-dl/2/dxOh2aXX4n-wTjc_tDXeEQ/1570500280/191007/106G7PDUDTUC9BHWIZBGR.mp4?name=HorribleSubsBabylon011080pr527.x.mp4-rh-108.mp4.mp4', 'https://www240.playercdn.net/p-dl/2/wlTFfffA6sFaQ8lQPxQmRw/1570500280/191007/105G7PDTAY0DF8GEYLCNI.mp4?name=HorribleSubsBabylon011080pr527.x.mp4-rh-108.mp4-480.mp4'], 'G:/KSD/Babylon_Episode_001.mp4'], ['Babylon Episode 002', 'https://kissanime.ru/Anime/Babylon/Episode-002?id=162739', 'https://www.rapidvideo.com/d/G7PDQPHIO0', ['https://www142.playercdn.net/p-dl/3/75m_7YidYuRc-Ic6zrHnNw/1570500297/191007/104G7PDSAY78LC70IWE6X.mp4?name=HorribleSubsBabylon021080pr440.x.mp4-rh-346.mp4-1080.mp4', 'https://www315.playercdn.net/p-dl/1/bOeFxtOCQy3fxyjdoq8LbA/1570500297/191007/104G7PDSA7YJ3L8XGTMWR.mp4?name=HorribleSubsBabylon021080pr440.x.mp4-rh-346.mp4.mp4', 'https://www93.playercdn.net/p-dl/0/cgTMWfiX4QqBvfc5xqM_ig/1570500297/191007/105G7PDTBJ49QUAJ2KJMY.mp4?name=HorribleSubsBabylon021080pr440.x.mp4-rh-346.mp4-480.mp4'], 'G:/KSD/Babylon_Episode_002.mp4'], ['Babylon Episode 003', 'https://kissanime.ru/Anime/Babylon/Episode-003?id=162737', 'https://www.rapidvideo.com/d/G7PDTNX2K5', ['https://www366.playercdn.net/p-dl/1/yXGOMzEy1F1dG6DaksAtSA/1570500305/191007/106G7PDVEP4E69I1QK9PI.mp4?name=HorribleSubsBabylon031080pr447.x.mp4-rh-528.mp4-1080.mp4', 'https://www198.playercdn.net/p-dl/1/-IppCflRmwx1tUmwuS8L-g/1570500305/191007/106G7PDVE6HRBJ0CNCXDK.mp4?name=HorribleSubsBabylon031080pr447.x.mp4-rh-528.mp4.mp4', 'https://www260.playercdn.net/p-dl/0/0Pm2cwxTw6MC7C2caPmXeQ/1570500305/191007/107G7PDWFUCIIX0O1UT34.mp4?name=HorribleSubsBabylon031080pr447.x.mp4-rh-528.mp4-480.mp4'], 'G:/KSD/Babylon_Episode_003.mp4']]

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

        # else:
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
                # print("Download Manager: Empty Queue")
                time.sleep(1)


def scrape_urls(url):
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("C:/chromedriver.exe")  # , options=chrome_options
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


class SeleniumWorker(QtCore.QObject):
    progressChanged = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal(bool)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def doWork(self):
        total_episodes = 0
        progress = 0
        driver = webdriver.Chrome("C:/chromedriver.exe")  # , options=chrome_options
        driver.get(self.url)

        try:
            wait = WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div[3]/div/div/ul/li/a"), "Home")
        )
        except NoSuchElementException:
            print("not Found")

        episodes = driver.find_elements_by_xpath("/html/body/div/div[4]/div/div[2]/div[2]/div[2]/table/tbody/tr")[2:]

        for episode in reversed(episodes):
            elem = episode.find_element_by_tag_name("td").find_element_by_tag_name("a")
            if "Episode" in elem.text:
                ep = [elem.text, elem.get_attribute("href")]
                episode_list.append(ep)
                total_episodes += 1

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
            progress += 100 / total_episodes
            self.progressChanged.emit(progress)

        driver.close()
        self.finished.emit(True)


class WindowScrapper(QtWidgets.QWidget):
    sig = pyqtSignal(str)

    def __init__(self, parent=None):
        # QWindowsStyle
        QtWidgets.QWidget.__init__(self, parent)
        # self.setStyle(QFusionStyle)
        self.setWindowTitle("KSD - Extracter")
        self.setMinimumWidth(int(resolution.width() / 3))
        self.setMinimumHeight(int(resolution.height() / 1.5))

        self.input_url = QtWidgets.QLineEdit(self)
        self.input_url.setText("https://kissanime.ru/Anime/Babylon")
        self.progressbar = QProgressBar(self)
        self.progressbar.setRange(0, 100)
        self.label = QLabel('URL')
        self.btn_startScraping = QPushButton(self)

        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.label, 0, 0, 1, 2)
        self.grid.addWidget(self.input_url, 0, 2, 1, 8)
        self.grid.addWidget(self.btn_startScraping, 1, 2, 1, 5)
        self.grid.addWidget(self.progressbar, 2, 0, 1, 10)

        self.grid.setContentsMargins(7, 7, 7, 7)
        self.setLayout(self.grid)

        self.btn_startScraping.clicked.connect(self.start_scraping)
        self.dialog = WindowDownloader()

    def start_scraping(self):
        self.hide()
        self.dialog.show()
        # self.progressbar.setValue(0)
        # self.btn_startScraping.setEnabled(False)
        # self.threadd = QtCore.QThread()
        # self.worker = SeleniumWorker(str(self.input_url.text()))
        # self.worker.moveToThread(self.threadd)
        # self.threadd.started.connect(self.worker.doWork)
        # self.threadd.start()
        # self.worker.progressChanged.connect(self.progressbar.setValue, QtCore.Qt.QueuedConnection)
        # self.worker.finished.connect(self.is_finished)

    def is_finished(self, result):
        if result is True:
            print("Finished")
            print(episode_list)
            self.threadd.quit()
            # self.btn_startScraping.setEnabled(True)
            # self.hide()
            # self.dialog.show()


class WindowDownloader(QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.setWindowTitle("KSD - Downloader")
        self.setMinimumWidth(int(resolution.width() / 1.5))
        self.setMinimumHeight(int(resolution.height() / 1.5))

        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(QLabel('#'), 0, 0, 1, 1)
        self.grid.addWidget(QLabel('Quality'), 0, 1, 1, 3)
        self.grid.addWidget(QLabel('Download'), 0, 3, 1, 1)

        self.grid.addWidget(QLabel('1080'), 1, 1, 1, 1)
        self.grid.addWidget(QLabel('720'), 1, 2, 1, 1)
        self.grid.addWidget(QLabel('360'), 1, 3, 1, 1)

        # for episode in episode_list:

        self.setLayout(self.grid)


if __name__ == "__main__":
    # download_manager = DownloadManager()
    # dm_thread = DownloadManagerThread()
    # dm_thread.start()
    #
    # data = scrape_urls("https://kissanime.ru/Anime/Black-Clover-TV-Dub")
    #
    # for item in data:
    #     # print(item)
    #     download_manager.add(item)

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()
    myapp = WindowScrapper()
    myapp.show()
    myapp.move(resolution.center() - myapp.rect().center())
    sys.exit(app.exec_())

    # dark_palette = QPalette()
    #
    # dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    # dark_palette.setColor(QPalette.WindowText, Qt.white)
    # dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    # dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    # dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    # dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    # dark_palette.setColor(QPalette.Text, Qt.white)
    # dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    # dark_palette.setColor(QPalette.ButtonText, Qt.white)
    # dark_palette.setColor(QPalette.BrightText, Qt.red)
    # dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    # dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    # dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    #
    # app.setPalette(dark_palette)
    # app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
else:
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()
