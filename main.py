from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import glob
import os.path
import pandas

keywords_input = input("Insert keywords you would like to check separated by comma: ")
keywords = list(keywords_input.split(","))

def find_file():
    list_of_files = glob.glob('/Users/timothyfisher/Downloads/*.csv')
    latest_file = max(list_of_files, key=os.path.getmtime)

    return latest_file

chrome_driver_path = "/Users/timothyfisher/PycharmProjects/chromedriver-3"

s = Service(chrome_driver_path)

driver = webdriver.Chrome(service=s)

driver.get("https://trends.google.com/trends/?geo=GB")

def trends_search():

    files_list = []
    count = 0

    for keyword in keywords:

        if keyword == keywords[0]:

            search_bar = driver.find_element(By.XPATH, "//*[@id='input-254']")
            search_bar.send_keys(keywords[0])
            time.sleep(2)
            search_bar.send_keys(Keys.ENTER)

            time.sleep(4)
            time_frame_button = driver.find_element(By.TAG_NAME, 'custom-date-picker')
            time_frame_button.click()

            time.sleep(5)
            time_frame = driver.find_element(By.XPATH, '/html/body/div[8]/md-select-menu/md-content/md-option[6]/div')
            time_frame.click()

            time.sleep(2)

            download_file = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/md-content/div/div/div[1]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]')
            download_file.click()

            time.sleep(4)
            files_list.append(find_file())


        else:

            for n in range(len(keywords[count])):
                time.sleep(1)
                search_bar = driver.find_element(By.XPATH,
                                                 '/html/body/div[3]/div[2]/div/header/div/div[3]/ng-transclude/div[2]/explore-pills/div/div/explore-search-term/div/ng-include/md-autocomplete/md-autocomplete-wrap/input')
                search_bar.send_keys(Keys.BACKSPACE)

            time.sleep(2)
            search_bar.send_keys(keyword)
            print(keyword)
            search_bar.send_keys(Keys.ENTER)

            time.sleep(3)

            download_file = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/md-content/div/div/div[1]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]')
            download_file.click()

            time.sleep(3)

            files_list.append(find_file())

            count+=1
            print(f"FILES LIST: {files_list}")

    driver.close()
    df = pandas.concat((pandas.read_csv(file) for file in files_list), axis=1)
    df.to_csv('result.csv')
    print(f"DF: {df}")

trends_search()