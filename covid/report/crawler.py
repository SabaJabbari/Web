import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By




def get_flumart_excel(country_code):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": r"C:/Users/sabaj/Downloads/a",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        main_url = 'https://apps.who.int/flumart/Default?ReportNo=13'
        driver.get(main_url)
    except:
        print("Server Error in '/flumart' Application.")
    sleep(5)
    select_element = driver.find_element(By.ID, 'fluid_list_countries')
    select_object = Select(select_element)
    select_object.select_by_index(country_code)
    driver.find_element(By.ID, 'ctl_ViewReport').click()

    i = 0
    while i < 2:
        el = driver.find_element(By.ID, 'ctl_ReportViewer_ctl05_ctl03_ctl00')
        try:
            sleep(20)
            driver.find_element(By.ID, 'ctl_ReportViewer_ctl05_ctl04_ctl00_ButtonImgDown').click()
            ReportViewer = driver.find_element(By.ID, 'ctl_ReportViewer_ctl05_ctl04_ctl00_Menu')
            ReportViewer_a = ReportViewer.find_elements(By.TAG_NAME, 'a')
            ReportViewer_a[1].click()
            base_path = 'C:/Users/sabaj/Downloads/a'
            return base_path + str(getDownLoadedFileName(driver, 5))
        except:
            i += 1
            sleep(3)


def getDownLoadedFileName(driver, waitTime):
    driver.execute_script("window.open()")
    # switch to new tab
    driver.switch_to.window(driver.window_handles[-1])
    # navigate to chrome downloads
    driver.get('chrome://downloads')
    # define the endTime
    endTime = time.time()+waitTime
    while True:
        try:
            # get downloaded percentage
            downloadPercentage = driver.execute_script(
                "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            if downloadPercentage == 100:
                # return the file name once the download is completed
                return driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
        except:
            pass
        time.sleep(1)
        if time.time() > endTime:
            break