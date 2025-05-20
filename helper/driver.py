import os
import zipfile
import requests
import env
import shutil
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

def get_driver_path():
    """Returns the path to the auto-downloaded ChromeDriver."""
    return ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()

def update_driver():
   pass

def download_driver(driver_path, system):
    r = requests.get(env.URL_CHROME_DRIVER_LATEST_RELEASE)
    latest_version = r.text
    if system == "Windows":
        url = f'https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.94/win32/chrome-win32.zip'
    elif system == "Darwin":
        url = f'https://chromedriver.storage.googleapis.com/{latest_version}/chromedriver_mac64.zip'
    elif system == "Linux":
        url = f'https://chromedriver.storage.googleapis.com/{latest_version}/chromedriver_linux64.zip'

    response = requests.get(url, stream=True)
    zip_file_path = os.path.join(os.path.dirname(
        driver_path), os.path.basename(url))
    with open(zip_file_path, "wb") as handle:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep alive chunks
                handle.write(chunk)
    extracted_dir = os.path.splitext(zip_file_path)[0]
    with zipfile.ZipFile(zip_file_path, "r") as zip_file:
        zip_file.extractall(extracted_dir)
    os.remove(zip_file_path)

    driver = os.listdir(extracted_dir)[0]
    os.rename(os.path.join(extracted_dir, driver), driver_path)
    shutil.rmtree(extracted_dir, ignore_errors=True)

    os.chmod(driver_path, 0o755)
    # way to note which chromedriver version is installed
    open(os.path.join(os.path.dirname(driver_path),
                      "{}.txt".format(latest_version)), "w").close()
