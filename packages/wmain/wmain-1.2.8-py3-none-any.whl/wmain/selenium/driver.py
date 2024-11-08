from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.edge import service
from wmain.requests import WSession
from wmain.base import create_dir, execute_powershell
from typing import Union, List
import time
import zipfile
import os
VERSION = "__version__"
EDGE_DIR_NAME = "edge"
EDGE_FILE_NAME = "msedgedriver.exe"
edge_zip_url = f"https://msedgedriver.azureedge.net/{VERSION}/edgedriver_win64.zip"

def get_edge_driver_zip_url(version: str):
    return edge_zip_url.replace(VERSION, version)


def download_edge_driver(session: WSession, version: str, dir: str, overwrite: bool=False):
    create_dir(dir)
    file = dir.rstrip("/") + f"/{EDGE_DIR_NAME}_{version}.zip"
    if not overwrite and os.path.exists(file):
        return
    session.get(get_edge_driver_zip_url(version)).save(file)
    extract_edge_driver_zip(file)
    

def extract_edge_driver_zip(file: str):
    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(os.path.dirname(file))

def guess_edge_version():
    return execute_powershell('(Get-AppxPackage -Name Microsoft.MicrosoftEdge.Stable).Version').strip()

class WEdgeDriver:
    driver: Edge = None
    
    def __init__(self, file: str):
        self.__srv = service.Service(file)
        self.__options = EdgeOptions()
    
    def start(self):
        self.__edge = Edge(options=self.__options, service=self.__srv)
        self.driver = self.__edge
    
    def option_headless(self):
        self.__options.add_argument('headless')

    def option_window_size(self, width, height):
        self.__options.add_argument(f'window-size={width}x{height}')

    def option_no_images(self):
        self.__options.add_argument('blink-settings=imagesEnabled=false')

    def option_no_gpu(self):
        self.__options.add_argument('disable-gpu')

    def option_no_music(self):
        self.__options.add_argument('--mute-audio')

    def option_maxsize(self):
        self.__options.add_argument('--start-maximized')
    
    def click_by_xpath(self, xpath: str):
        self.wait_for_element(xpath).click()

    def send_keys_by_xpath(self, xpath: str, keys: str):
        self.wait_for_element(xpath).send_keys(keys)
    
    def get_elements_by_xpath(self, xpath: str) -> List[WebElement]:
        return self.__edge.find_elements(By.XPATH, xpath)
    
    def get(self, url: str):
        self.__edge.get(str(url))
    
    def wait_for_element(self, xpath: str, timeout: float=10, step: float=0.2) -> Union[None, WebElement]:
        while timeout > 0:
            try:
                element = self.__edge.find_element(By.XPATH, xpath)
                self.js_scroll_to_element(element)
                return element
            except Exception:
                time.sleep(step)
                timeout -= step
        return None
    
    def js_scroll_to_element(self, element: WebElement):
        self.__edge.execute_script("arguments[0].scrollIntoView();", element)
    
    def switch_to_end_window(self):
        windows = self.__edge.window_handles
        self.__edge.switch_to.window(windows[-1])

    def js(self, js_path: str, func: str, args: list):
        start = f'return {func}({args})\n'
        with open(js_path, 'r') as f:
            return self.__edge.execute_script(start + f.read())
        
class WEdgeDownloader:

    def __init__(self, path: str='./driver', auto_download: bool=True, session: WSession=WSession()):
        self.session = session
        self.path = path.strip() + "/" + EDGE_DIR_NAME
        if auto_download:
            self.start()

    def __download(self, version: str, overwrite: bool=False):
        version = version.strip()
        download_edge_driver(self.session, version, self.path, overwrite)
            
    
    def __call__(self, version: str = guess_edge_version(), overwrite: bool=False):
        self.__download(version, overwrite)
        
    def start(self, version: str = guess_edge_version(), overwrite: bool=False):
        self.__download(version, overwrite)
        
    def get_driver(self) -> Union[None, WEdgeDriver]:
        for filename in os.listdir(self.path):
            if "driver" in filename:
                return WEdgeDriver(self.path + "/" + filename)
        return None